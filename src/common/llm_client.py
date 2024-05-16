import json
from typing import Callable, List, Optional, Dict
from openai import OpenAI
import requests

from src.config import Config
from ..types.llm_tools import FunctionTool
from ..types.llm_messages import Message


class LLMClient:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.get_openai_api_key()
        self.client = OpenAI(api_key=self.api_key)

    def inference(
        self,
        model_id: str,
        messages: List[Message],
        tools: List[FunctionTool],
        command_function_tools_mapping: Dict[str, Callable],
        tool_choice: Optional[str] = None,
    ) -> Dict[str, str]:
        try:
            tool_choice = tool_choice if tool_choice else ("auto" if tools else None)

            response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
                response_format={"type": "json_object"},
                tools=tools,
                tool_choice=tool_choice,
            )

        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "type": "APIConnectionError",
                "message": "Check your network settings, proxy configuration, SSL certificates, or firewall rules.",
            }
        except requests.exceptions.Timeout:
            return {
                "status": "error",
                "type": "APITimeoutError",
                "message": "Request timed out. Retry your request after a brief wait.",
            }
        except requests.exceptions.HTTPError as e:
            return self.handle_http_error(e)
        except Exception as e:
            return {
                "status": "error",
                "type": "UnexpectedError",
                "message": str(e),
            }

        try:
            response_message = response.choices[0].message
            json.loads(response_message.content)
        except json.JSONDecodeError:
            return {
                "status": "error",
                "type": "InvalidResponse",
                "message": "The response from the model was not a valid JSON. \n\n"
                + response_message.content.strip(),
            }

        # check if the model responded with a tool call
        if response_message.tool_calls:
            # call the function
            messages.append(
                response_message
            )  # extend conversation with assistant's reply
            # send the info for each function call and function response to the model
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_to_call = command_function_tools_mapping[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )  # extend conversation with function response

            second_response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
                response_format={"type": "json_object"},
            )

            try:
                second_response_message = second_response.choices[0].message
                json.loads(second_response_message.content)
                return {
                    "status": "success",
                    "type": "InferenceResponseWithToolCalls",
                    "message": second_response_message.content,
                }
            except json.JSONDecodeError:
                return {
                    "status": "error",
                    "type": "InvalidResponseWithToolCalls",
                    "message": "The response from the model was not a valid JSON. \n\n"
                    + second_response_message.content.strip(),
                }

        return {
            "status": "success",
            "type": "InferenceResponse",
            "message": response_message.content,
        }

    def handle_http_error(self, e: requests.exceptions.HTTPError) -> Dict[str, str]:
        status_code = e.response.status_code
        type = "HTTPError"
        message = "An HTTP error occurred."
        if status_code == 401:
            type = "AuthenticationError"
            message = "Your API key or token was invalid, expired, or revoked. Check your API key or token."
        elif status_code == 400:
            type = "BadRequestError"
            message = "Your request was malformed or missing some required parameters."
        elif status_code == 404:
            type = "NotFoundError"
            message = (
                "Requested resource does not exist. Check your resource identifier."
            )
        elif status_code == 429:
            type = "RateLimitError"
            message = "You have hit your assigned rate limit. Pace your requests."
        elif status_code == 500:
            type = "InternalServerError"
            message = "Issue on our side. Retry your request after a brief wait."
        return {"status": "error", "type": type, "message": message}

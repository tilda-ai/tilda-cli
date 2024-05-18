import json
import requests
from typing import Callable, Dict, List, Optional

from src.config import Config
from ..types.llm_tools import FunctionTool
from ..types.llm_messages import Message
from .tool_handler import ToolHandler
from openai import OpenAI


class LLMClient:
    def __init__(self, tools_mapping: Dict[str, Callable] = {}):
        self.config = Config()
        self.api_key = self.config.get_openai_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.tool_handler = ToolHandler(tools_mapping)

    def inference(
        self,
        model_id: str,
        messages: List[Message],
        tools: List[FunctionTool],
        tool_choice: Optional[str] = None,
    ) -> Dict[str, str]:
        tool_choice = tool_choice or ("auto" if tools else None)
        
        try:
            response = self._make_request(model_id, messages, tools, tool_choice)
        except Exception as e:
            return self._handle_exception(e)
        
        return self._process_response(model_id, response, messages)

    def _make_request(self, model_id, messages, tools, tool_choice):
        return self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            response_format={"type": "json_object"},
            tools=tools,
            tool_choice=tool_choice,
        )

    def _process_response(self, model_id, response, messages):
        response_message = response.choices[0].message
        validation_result = self._validate_json_response(
            response_message, "InferenceResponse"
        )

        if validation_result["status"] == "error":
            return validation_result

        if response_message.tool_calls:
            return self._handle_tool_calls(
                model_id, response_message, response, messages
            )

        return validation_result

    def _handle_tool_calls(self, model_id, response_message, response, messages):
        messages.append(response_message)  # extend conversation
        updated_messages = self.tool_handler.handle_tool_calls(
            response["tool_calls"], messages
        )
        try:
            second_response = self._make_request(model_id, updated_messages, [], None)
        except Exception as e:
            return self._handle_exception(e)

        second_response_message = second_response.choices[0].message
        return self._validate_json_response(
            second_response_message, "InferenceResponseWithToolCalls"
        )

    def _validate_json_response(self, message, response_type):
        try:
            json.loads(message.content)
            return {
                "status": "success",
                "type": response_type,
                "message": message.content,
            }
        except json.JSONDecodeError:
            # handle duplicated response
            deduped_response_object = self._dedupe_json_objects(message.content)
            
            if deduped_response_object:
                try:
                    json.loads(deduped_response_object)
                    return {
                        "status": "success",
                        "type": response_type,
                        "message": deduped_response_object,
                    }
                except json.JSONDecodeError:
                    return {
                        "status": "error",
                        "type": f"Invalid{response_type}",
                        "message": "Invalid JSON received: \n\n" + message.content.strip(),
                    }
                    
            return {
                "status": "error",
                "type": f"Invalid{response_type}",
                "message": "Invalid JSON received: \n\n" + message.content.strip(),
            }

    def _dedupe_json_objects(input_string) -> str | None:
        try: 
            # Replace all line breaks with spaces
            text = input_string.replace('\n', ' ')
            
            # Split the string by whitespace and then join with a single space
            clean_text = ' '.join(text.split())

            sprinkled_text = clean_text.replace('} {', '}~~!~~{')
            
            # Split the cleaned string into separate JSON objects
            json_objects = sprinkled_text.split('~~!~~')

            return json_objects[0]
        except Exception as e:
            return None

    def _handle_exception(self, e):
        if isinstance(e, requests.exceptions.HTTPError):
            return self.handle_http_error(e)
        elif isinstance(e, requests.exceptions.ConnectionError):
            return {
                "status": "error",
                "type": "APIConnectionError",
                "message": "Check your network settings, proxy configuration, SSL certificates, or firewall rules.",
            }
        elif isinstance(e, requests.exceptions.Timeout):
            return {
                "status": "error",
                "type": "APITimeoutError",
                "message": "Request timed out. Retry your request after a brief wait.",
            }
        else:
            return {
                "status": "error",
                "type": "UnexpectedError",
                "message": str(e),
            }

    def handle_http_error(self, e):
        error_map = {
            401: ("AuthenticationError", "Invalid, expired, or revoked API key."),
            400: ("BadRequestError", "Malformed request or missing parameters."),
            404: ("NotFoundError", "Resource not found."),
            429: ("RateLimitError", "Rate limit exceeded."),
            500: ("InternalServerError", "Server error. Retry later."),
        }
        error_type, message = error_map.get(
            e.response.status_code, ("HTTPError", "An HTTP error occurred.")
        )
        return {"status": "error", "type": error_type, "message": message}

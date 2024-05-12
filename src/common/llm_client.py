from typing import List, Optional, Dict
import openai
import requests

from src.config import Config
from ..types.llm_tools import FunctionTool
from ..types.llm_messages import Message


class LLMClient:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.get_openai_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)

    def inference(
        self,
        model_id: str,
        messages: List[Message],
        tools: List[FunctionTool],
        tool_choice: Optional[str] = None,
    ) -> Dict[str, str]:
        try:
            tool_choice = tool_choice if tool_choice else ("auto" if tools else None)
            chat_completion = self.client.ChatCompletion.create(
                messages=messages,
                model=model_id,
                response_format={"type": "json_object"},
                tools=tools,
                tool_choice=tool_choice,
            )
            response_content = chat_completion["choices"][0]["message"]["content"]
            return {
                "status": "success",
                type: "InferenceSuccess",
                "message": response_content,
            }
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

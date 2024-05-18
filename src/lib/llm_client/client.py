from typing import Callable, Dict, List, Optional

from src.config import Config
from ..types.llm_tools import FunctionTool
from ..types.llm_messages import Message
from .tool_handler import ToolHandler
from .error_handler import ErrorHandler
from .response_validator import ResponseValidator
from openai import OpenAI


class LLMClient:
    def __init__(self, tools_mapping: Dict[str, Callable] = None):
        self.config = Config()
        self.api_key = self.config.get_openai_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.tool_handler = ToolHandler(tools_mapping or {})

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
            return ErrorHandler.handle_exception(e)  # Use ErrorHandler

        return self._process_response(model_id, response, messages)

    def _make_request(
        self,
        model_id: str,
        messages: List[Message],
        tools: List[FunctionTool],
        tool_choice: Optional[str],
    ) -> dict:
        return self.client.chat.completions.create(
            model=model_id,
            messages=messages,
            response_format={"type": "json_object"},
            tools=tools,
            tool_choice=tool_choice,
        )

    def _process_response(
        self, model_id: str, response: dict, messages: List[Message]
    ) -> Dict[str, str]:
        response_message = response.choices[0].message
        validation_result = ResponseValidator.validate_json_response(
            response_message, "InferenceResponse"
        )

        if validation_result["status"] == "error":
            return validation_result

        if response_message.tool_calls:
            return self._handle_tool_calls(
                model_id, response_message, response, messages
            )

        return validation_result

    def _handle_tool_calls(
        self,
        model_id: str,
        response_message: dict,
        response: dict,
        messages: List[Message],
    ) -> Dict[str, str]:
        messages.append(response_message)  # extend conversation
        updated_messages = self.tool_handler.handle_tool_calls(
            response["tool_calls"], messages
        )
        
        try:
            second_response = self._make_request(model_id, updated_messages, [], None)
        except Exception as e:
            return ErrorHandler.handle_exception(e)  # Use ErrorHandler

        second_response_message = second_response.choices[0].message
        return ResponseValidator.validate_json_response(
            second_response_message, "InferenceResponseWithToolCalls"
        )

import sys
from typing import Callable, Dict, List, Optional

from src.config import Config
from ..types.llm_tools import FunctionTool
from ..types.llm_messages import Message
from .tool_handler import ToolHandler
from .response_validator import ResponseValidator
from openai import OpenAI


class LLMClient:
    def __init__(self, tools_mapping: Dict[str, Callable] = None):
        self.config = Config()
        self.api_key = self.config.get_llm_api_key()
        self.client = OpenAI(api_key=self.api_key)
        self.tool_handler = ToolHandler(tools_mapping or {})
        self.retry_count = 0

    def inference(
        self,
        model_id: str,
        messages: List[Message],
        tools: List[FunctionTool],
        schema,
        tool_choice: Optional[str] = None,
    ) -> Dict[str, str]:
        tool_choice = tool_choice or ("auto" if tools else None)

        response = self._make_request(model_id, messages, tools, tool_choice)

        return self._process_response(model_id, response, messages, schema)

    def _make_request(
        self,
        model_id: str,
        messages: List[Message],
        tools: List[FunctionTool],
        tool_choice: Optional[str],
    ) -> dict:
        try:
            response = self.client.chat.completions.create(
                model=model_id,
                messages=messages,
                response_format={"type": "json_object"},
                tools=tools,
                tool_choice=tool_choice,
            )
        except Exception as e:
            sys.stderr.write(str(e))
            sys.exit(1)

        return response

    def _process_response(
        self, model_id: str, response: dict, messages: List[Message], schema
    ) -> Dict[str, str]:
        response_message = response.choices[0].message
        validation_result = ResponseValidator.validate_json_response(
            response_message, "InferenceResponse", schema=schema
        )

        if validation_result["status"] == "error":
            if self.retry_count == 1:
                sys.stderr.write(
                    f"Failed to validate response after 2 attempts: {validation_result['message']}"
                )
                sys.exit(1)
            return self._handle_retry_request(
                model_id, response_message, messages, schema, error_message=validation_result["message"]
            )
            
        if response_message.tool_calls:
            return self._handle_tool_calls(
                model_id, response_message, response, messages, schema
            )

        return validation_result

    def _handle_retry_request(
        self,
        model_id: str,
        response_message: Message,
        messages: List[Message],
        schema,
        error_message: str,
    ) -> Dict[str, str]:
        self.retry_count += 1
        updated_messages = messages.copy()
        updated_messages.append(response_message)
        updated_messages.append(
            {
                "role": "system",
                "name": "response_validation_error_message",
                "content": error_message,
            }
        )
        

        retry_response = self._make_request(model_id, updated_messages, [], None)
        retry_response_message = retry_response.choices[0].message

        return ResponseValidator.validate_json_response(
            retry_response_message, "InferenceResponse", schema=schema
        )

    def _handle_tool_calls(
        self,
        model_id: str,
        response_message: dict,
        response: dict,
        messages: List[Message],
        schema,
    ) -> Dict[str, str]:
        messages.append(response_message)  # extend conversation
        updated_messages = self.tool_handler.handle_tool_calls(
            response["tool_calls"], messages
        )

        second_response = self._make_request(model_id, updated_messages, [], None)
        second_response_message = second_response.choices[0].message

        return ResponseValidator.validate_json_response(
            second_response_message, "InferenceResponseWithToolCalls", schema=schema
        )

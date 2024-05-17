import json
from typing import Callable, Dict


class ToolHandler:
    def __init__(self, command_function_tools_mapping: Dict[str, Callable] = {}):
        self.command_function_tools_mapping = command_function_tools_mapping

    def handle_tool_calls(self, tool_calls, messages):
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            try:
                function_to_call = self.command_function_tools_mapping[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )
            except Exception as e:
                # Handle exceptions and potentially log them
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": str(e),
                    }
                )
        return messages

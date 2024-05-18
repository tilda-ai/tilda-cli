from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class SystemMessage:
    role: str
    content: str
    name: Optional[str] = None


@dataclass
class UserMessage:
    role: str
    content: Union[str, List[str]]
    name: Optional[str] = None


@dataclass
class AssistantMessage:
    role: str
    content: Optional[str] = None
    name: Optional[str] = None
    tool_calls: Optional[List["ToolCall"]] = (
        None  # Assuming ToolCall is defined elsewhere
    )


@dataclass
class ToolMessage:
    role: str
    content: str
    tool_call_id: str


@dataclass
class ToolCall:
    function_name: str
    arguments: dict


@dataclass
class Message:
    system_message: Optional[SystemMessage] = None
    user_message: Optional[UserMessage] = None
    assistant_message: Optional[AssistantMessage] = None
    tool_message: Optional[ToolMessage] = None

from dataclasses import dataclass
from typing import Optional

@dataclass
class TerminalCommandArgs:
    prompt: str
    scope: Optional[str] = None
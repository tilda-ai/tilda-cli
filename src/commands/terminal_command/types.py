from dataclasses import dataclass
from typing import Optional

@dataclass
class TerminalCommandArgs:
    prompt: str
    dry: Optional[bool] = False
    mock: Optional[bool] = False

from enum import Enum
from dataclasses import dataclass
from typing import Optional

@dataclass
class InitCommandArgs:
    skip_auto_config: Optional[bool] = False
    dry: Optional[bool] = False
    mock: Optional[bool] = False
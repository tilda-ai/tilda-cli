from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class JSONSchema:
    type: str
    properties: Dict[str, 'JSONSchema'] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    additionalProperties: Optional[bool] = None

@dataclass
class FunctionTool:
    type: str  # Currently, only 'function' is supported
    name: str
    description: Optional[str] = None
    parameters: Optional[JSONSchema] = None
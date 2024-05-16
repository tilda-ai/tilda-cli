from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any

@dataclass
class JSONSchema:
    type: str
    properties: Dict[str, 'JSONSchema'] = field(default_factory=dict)
    required: List[str] = field(default_factory=list)
    additionalProperties: Optional[bool] = None
    description: Optional[str] = None  # Adding description here for inline documentation of properties.
    enum: Optional[List[Any]] = None  # Adding enum for constrained values.

    def to_dict(self):
        # Custom serialization to handle nested JSONSchema objects and optional fields.
        schema_dict = {"type": self.type}
        if self.properties:
            schema_dict["properties"] = {k: v.to_dict() for k, v in self.properties.items()}
        if self.required:
            schema_dict["required"] = self.required
        if self.additionalProperties is not None:
            schema_dict["additionalProperties"] = self.additionalProperties
        if self.description:
            schema_dict["description"] = self.description
        if self.enum:
            schema_dict["enum"] = self.enum
        return schema_dict

@dataclass
class FunctionTool:
    type: str  # Currently, only 'function' is supported
    function: Dict[str, Any]  # Changed to match your required structure

    def to_dict(self):
        return {
            "type": self.type,
            "function": self.function
        }
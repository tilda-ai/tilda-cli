schema = {
    "type": "object",
    "properties": {
        "completions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "content": {"type": "string"},
                    "chainable": {"type": "boolean"},
                    "chain_delimiter": {"type": ["string", "null"]},
                    "sudo": {"type": "boolean"},
                    "dangerous": {"type": "boolean"},
                    "interactive": {"type": "boolean"},
                    "order": {"type": "integer"},
                    "confidence": {"type": "integer", "minimum": 0, "maximum": 100},
                    "sources": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2
                    }
                },
                "required": ["description", "content", "chainable", "chain_delimiter", "sudo", "dangerous", "interactive", "order", "confidence", "sources"]
            }
        }
    },
    "required": ["completions"]
}
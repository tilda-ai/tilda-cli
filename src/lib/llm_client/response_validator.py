import json
from typing import Dict, Optional
import jsonschema
from jsonschema import validate

class ResponseValidator:
    @staticmethod
    def validate_json_response(message: dict, response_type: str, schema) -> Dict[str, str]:
        try:
            response_content = json.loads(message.content)
            # Validate against schema
            validate(instance=response_content, schema=schema)
            return {
                "status": "success",
                "type": response_type,
                "message": message.content,
            }
        except json.JSONDecodeError as e:
            # handle duplicated response
            deduped_response_object = ResponseValidator._dedupe_json_objects(
                message.content
            )

            if deduped_response_object:
                try:
                    response_content = json.loads(deduped_response_object)
                    # Validate against schema
                    validate(instance=response_content, schema=schema)
                    return {
                        "status": "success",
                        "type": response_type,
                        "message": deduped_response_object,
                    }
                except json.JSONDecodeError as inner_e:
                    return {
                        "status": "error",
                        "type": f"Invalid{response_type}",
                        "message": f"Invalid JSON received: \n\n{message.content.strip()}\nError: {inner_e}",
                    }
                except jsonschema.ValidationError as ve:
                    return {
                        "status": "error",
                        "type": f"Invalid{response_type}",
                        "message": f"JSON Schema validation error: {ve.message}\nInvalid JSON received: \n\n{deduped_response_object.strip()}"
                    }
            return {
                "status": "error",
                "type": f"Invalid{response_type}",
                "message": f"Invalid JSON received: \n\n{message.content.strip()}\nError: {e}",
            }
        except jsonschema.ValidationError as ve:
            return {
                "status": "error",
                "type": f"Invalid{response_type}",
                "message": f"JSON Schema validation error: {ve.message}\nInvalid JSON received: \n\n{message.content.strip()}"
            }

    @staticmethod
    def _dedupe_json_objects(input_string: str) -> Optional[str]:
        try:
            # Replace all line breaks with spaces
            flat_string = input_string.replace("\n", " ")
            # split the string by whitespace and then join with a single space
            clean_string = " ".join(flat_string.split())
            # sprinkle the string with a delimiter
            sprinkled_string = clean_string.replace("} {", "}~~!~~{")
            # break the string into json objects
            json_objects = sprinkled_string.split("~~!~~")

            return json_objects[0] if json_objects else None
        except Exception:
            return None

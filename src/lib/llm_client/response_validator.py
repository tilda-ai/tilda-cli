import json
from typing import Dict, Optional

#TODO: add schema validation
#TODO: add self rejection and reflection

class ResponseValidator:
    @staticmethod
    def validate_json_response(message: dict, response_type: str) -> Dict[str, str]:
        try:
            json.loads(message.content)
            return {
                "status": "success",
                "type": response_type,
                "message": message.content,
            }
        except json.JSONDecodeError:
            # handle duplicated response
            deduped_response_object = ResponseValidator._dedupe_json_objects(
                message.content
            )

            if deduped_response_object:
                try:
                    json.loads(deduped_response_object)
                    return {
                        "status": "success",
                        "type": response_type,
                        "message": deduped_response_object,
                    }
                except json.JSONDecodeError:
                    #TODO: return the error to the llm_client for re-processing (1 retry only)
                    return {
                        "status": "error",
                        "type": f"Invalid{response_type}",
                        "message": f"Invalid JSON received: \n\n{message.content.strip()}",
                    }

            return {
                "status": "error",
                "type": f"Invalid{response_type}",
                "message": f"Invalid JSON received: \n\n{message.content.strip()}",
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

from dataclasses import dataclass
from typing import List
import openai

from src.config import Config
    
@dataclass
class Example:
    role: str 
    name: str
    content: str

class LLMInferenceClient:
    def __init__(self):
        self.config = Config()
        self.api_key = self.config.get_openai_api_key()
        self.client = openai.OpenAI(api_key=self.api_key)

    def inference(self, model_id: str, system_prompt: str, examples: List[Example], user_prompt: str) -> str:
        try:
            chat_completion = self.client.ChatCompletion.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    *examples,
                    {"role": "user", "content": user_prompt.strip()},
                ],
                model=model_id,
                response_format={ "type": "json_object" }
            )
            response_content = chat_completion['choices'][0]['message']['content']
            return {'status': 'success', 'response': response_content}
        except openai.Error as e:
            return {'status': 'error', 'error_message': str(e)}
        except Exception as e:
            return {'status': 'error', 'error_message': 'An unexpected error occurred'}

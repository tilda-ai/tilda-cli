import ollama

from src.logger import logger
from src.config import Config


class Ollama:
    def __init__(self):
        try:
            config = Config()
            self.client = ollama.Client(config.get_ollama_api_endpoint())
            self.models = self.client.list()["models"]
            logger.info("Ollama available")
        except Exception:
            self.client = None
            logger.warning("Ollama not available")
            logger.warning("run ollama server to use ollama models otherwise use other models")

    def inference(self, model_id: str, prompt: str) -> str:
        response = self.client.generate(
            model=model_id,
            prompt=prompt.strip()
        )
        return response['response']

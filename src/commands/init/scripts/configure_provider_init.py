import os
from InquirerPy import prompt

from src.logger import logger
from ..enums.provider import Provider

def configure_provider_init(provider:Provider,base_path: str):
    
    questions = [
        {
            'type': 'password',
            'message': 'Please enter API key:',
            'name': 'API_key',
        }
    ]
        
    answers = prompt(questions)
    if answers['API_key'] is None:
        logger.error("API key cannot be empty.")
        raise Exception("API key cannot be empty.")
        
    update_tildaconfig(base_path, answers['API_key'], get_key_path(provider))
        

    

def update_tildaconfig(base_path: str, api_key: str, key_path:str):
    config_path = os.path.join(base_path, "tildaconfig.toml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = file.read()
        updated_config = config_data.replace("<YOUR_OPENAI_API_KEY>", api_key)
        with open(config_path, "w", encoding="utf-8") as file:
            file.write(updated_config)
        logger.info("tildaconfig.toml updated successfully.")
    else:
        logger.error("tildaconfig.toml does not exist.")
        

       
def get_key_path(provider:Provider):
    switcher = {
        Provider.OPENAI: "<YOUR_OPENAI_API_KEY>",
        Provider.CLAUDE: "<YOUR_CLAUDE_API_KEY>",
        Provider.GEMINI: "<YOUR_GENIMI_API_KEY>",
        Provider.OLLAMA: "<YOUR_OLLAMA_API_KEY>"
    }
    return switcher.get(provider, "Invalid provider")


        
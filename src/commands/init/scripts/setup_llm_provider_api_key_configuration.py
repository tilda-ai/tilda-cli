from pathlib import Path
from InquirerPy import prompt

from src.logger import logger
from ..enums.llm_providers import LLMProviders
from .update_tildaconfig import update_tildaconfig

def setup_llm_provider_api_key_configuration(current_directory_path: Path):
    if not current_directory_path.exists():
        logger.error("The directory [%s] does not exist.", current_directory_path)
        raise FileNotFoundError(f"The directory {current_directory_path} does not exist.")
    
    llm_provider = select_llm_provider_prompt()
    if llm_provider == "Skip":
        logger.info("Skipping API key configuration.")
        return
    
    placeholder_pattern = get_provider_key_placeholder(llm_provider)
    if placeholder_pattern == "Invalid provider":
        logger.error("Selected an invalid LLM provider.")
        raise ValueError("Invalid LLM provider selected.")
    
    provider_api_key = set_provider_api_key_prompt()
    update_tildaconfig(current_directory_path, placeholder_pattern, provider_api_key)

def get_provider_key_placeholder(provider: LLMProviders):
    switcher = {
        LLMProviders.OPENAI: "<YOUR_OPENAI_API_KEY>",
        LLMProviders.CLAUDE: "<YOUR_CLAUDE_API_KEY>",
        LLMProviders.GEMINI: "<YOUR_GENIMI_API_KEY>",
        LLMProviders.OLLAMA: "<YOUR_OLLAMA_API_KEY>"
    }
    return switcher.get(provider, "Invalid provider")

def select_llm_provider_prompt():
    llm_providers = [provider.value for provider in LLMProviders] + ["Skip"]
    llm_provdider_select_menu = [{"type": "list", "name": "provider", "message": "Please choose an option:", "choices": llm_providers}]
    response = prompt(llm_provdider_select_menu)
    return response["provider"]

def set_provider_api_key_prompt():
    api_key_user_input = [{'type': 'password', 'name': 'api_key', 'message': 'Please enter API key:'}]
    response = prompt(api_key_user_input)
    if not response['api_key']:
        logger.error("API key cannot be empty.")
        raise ValueError("API key cannot be empty.")
    return response['api_key']

from pathlib import Path
from InquirerPy import prompt

from src.logger import logger
from ..enums.llm_providers import LLMProviders
from .update_tildaconfig import update_tildaconfig

def setup_llm_provider_api_key_configuration(current_directory_path: Path):
    try:
        if not current_directory_path.exists():
            logger.error("The directory %s does not exist.", current_directory_path)
            return "Directory not found. Please check the path."

        llm_provider = select_llm_provider_prompt()
        if llm_provider == "Skip":
            logger.info("Skipping API key configuration.")
            return "Operation skipped by the user."

        placeholder_pattern = get_provider_key_placeholder(llm_provider)
        if placeholder_pattern == "Invalid provider":
            logger.error("Selected an invalid LLM provider.")
            return "Invalid LLM provider selected. Please select a valid provider."

        provider_api_key = set_provider_api_key_prompt()
        update_tildaconfig(current_directory_path, placeholder_pattern, provider_api_key)
        logger.info("Configuration updated successfully.")
        return "Configuration updated successfully."

    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        return f"An unexpected error occurred: {str(e)}"

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
    while True:  # Start a loop to keep asking until a valid input or 'skip'
        api_key_user_input = [{'type': 'password', 'name': 'api_key', 'message': 'Please enter API key (or type "skip" to skip):'}]
        response = prompt(api_key_user_input)
        if response['api_key'].strip().lower() == 'skip':  # Check if user types 'skip'
            logger.info("User chose to skip API key input.")
            return None  # Return None or another specific value to indicate skipping
        elif not response['api_key'].strip():  # Check if input is empty
            logger.error("API key cannot be empty.")
            print("API key cannot be empty. Please enter a valid API key or type 'skip' to skip.")
        else:
            return response['api_key']  # Return the API key if it's valid

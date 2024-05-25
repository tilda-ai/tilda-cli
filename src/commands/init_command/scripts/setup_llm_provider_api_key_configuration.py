from pathlib import Path
from InquirerPy import prompt

from src.config import Config
from src.lib.logger import Logger
from src.lib.utils.key_handler import KeyHandler

logger = Logger().get_logger()


def setup_llm_provider_api_key_configuration(current_directory_path: Path):
    try:
        if not current_directory_path.exists():
            logger.error("The directory %s does not exist.", current_directory_path)
            return "Directory not found. Please check the path."

        action = api_key_setup_action_prompt()

        if action == "Skip":
            logger.info("Skipping API key configuration.")
            return "Operation skipped by the user."
        logger.info("Skipping API key configuration.")
        
        api_key = set_api_key_prompt()
        KeyHandler.set_key(Config().get_llm_api_key_name(), api_key)
        
    except Exception as e:
        logger.error("An unexpected error occurred: %s", str(e))
        return f"An unexpected error occurred: {str(e)}"


def api_key_setup_action_prompt():
    menu = [
        {
            "type": "list",
            "name": "action",
            "message": "You can set your OpenAI API key now or skip it for later. What would you like to do?\nYou can find your API key at https://platform.openai.com/account/api-keys.",
            "choices": ["Insert", "Skip"],
        }
    ]
    response = prompt(menu)
    return response["action"]


def set_api_key_prompt():
    while True:  # Start a loop to keep asking until a valid input or 'skip'
        api_key_user_input = [
            {
                "type": "password",
                "name": "api_key",
                "message": 'Please enter API key (or type "skip" to skip):',
            }
        ]
        response = prompt(api_key_user_input)
        if response["api_key"].strip().lower() == "skip":  # Check if user types 'skip'
            logger.info("User chose to skip API key input.")
            return None
        elif not response["api_key"].strip():  # Check if input is empty
            logger.error("API key cannot be empty.")
            print(
                "API key cannot be empty. Please enter a valid API key or type 'skip' to skip."
            )
        else:
            return response["api_key"]  # Return the API key if it's valid

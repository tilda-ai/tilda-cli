import os
from pathlib import Path
from InquirerPy import prompt

from src.logger import logger
from ..enums.llm_providers import LLMProviders
from .update_tildaconfig import update_tildaconfig

def setup_llm_provider_api_key_configuration(current_directory_path: Path):
    llm_provider: LLMProviders = select_llm_provider_promot()
    placeholder_pattern = get_provider_key_placeholder(llm_provider)
    provider_api_key = set_provider_api_key_prompt()

    update_tildaconfig(current_directory_path, placeholder_pattern, provider_api_key)

def get_provider_key_placeholder(provider:LLMProviders):
    switcher = {
        LLMProviders.OPENAI: "<YOUR_OPENAI_API_KEY>",
        LLMProviders.CLAUDE: "<YOUR_CLAUDE_API_KEY>",
        LLMProviders.GEMINI: "<YOUR_GENIMI_API_KEY>",
        LLMProviders.OLLAMA: "<YOUR_OLLAMA_API_KEY>"
    }
    return switcher.get(provider, "Invalid provider")

def select_llm_provider_promot():
    # set choices with all provider values and exit value 
    choices = [provider.value for provider in LLMProviders] + ["Skip"]

    questions = [
        {
            "type": "list",
            "name": "option",
            "message": "Please choose an option:",
            "choices": choices
        }
    ]

    # Using prompt to collect user input based on defined questions
    response = prompt(questions)
    return response["option"]

def set_provider_api_key_prompt():
    questions = [
        {
            'type': 'password',
            'message': 'Please enter API key:',
            'name': 'api_key',
        }
    ]

    response = prompt(questions)

    if response['api_key'] is None:
        logger.error("API key cannot be empty.")
        raise Exception("API key cannot be empty.")

    return response['api_key']
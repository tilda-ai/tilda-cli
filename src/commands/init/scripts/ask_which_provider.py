from InquirerPy import prompt
from ..enums.provider import Provider

def ask_which_provider_to_use():
    # set choices with all provider values and exit value 
    choices = [provider.value for provider in Provider] + ["Exit"]
    
    questions = [
        {
            "type": "list",
            "name": "option",
            "message": "Please choose an option:",
            "choices": choices
        }
    ]
    
    # Using prompt to collect user input based on defined questions
    answers = prompt(questions)
    return answers["option"]

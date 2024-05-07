from InquirerPy import prompt

def prompt_error_resolution() -> str:
    response = prompt([{
            'type': 'list',
            'name': 'resolution',
            'message': 'How would you like to proceed?',
            'choices': ['Edit', 'Terminate']
        }], style={"pointer": "#00afff", "questionmark": "#ff9d00 bold"},)

    return response['resolution']

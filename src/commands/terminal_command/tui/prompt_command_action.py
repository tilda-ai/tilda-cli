from InquirerPy import prompt

def prompt_command_action() -> str:
    response = prompt([{
            'type': 'list',
            'name': 'action',
            'message': 'Do you want to run this command?',
            'choices': ['Run', 'Edit', 'Explain', 'Skip']
        }], style={"pointer": "#00afff", "questionmark": "#ff9d00 bold"},)

    return response['action']

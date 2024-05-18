def user_confirmation(prompt):
    """ Prompt the user for confirmation. """
    response = input(prompt).lower()
    return response in ["yes", "y"]

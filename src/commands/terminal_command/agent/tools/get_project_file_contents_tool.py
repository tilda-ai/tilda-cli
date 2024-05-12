from src.types.llm_tools import FunctionTool, JSONSchema

# Define the parameters for the function 'get_project_file_contents'
get_project_file_contents_params = JSONSchema(
    type='object',
    properties={
        'path': JSONSchema(type='string')
    },
    required=['path']
)

# Define the function tool
get_project_file_contents_tool = FunctionTool(
    type='function',
    name='get_project_file_contents',
    description='Retrieves the contents of the file at the specified path, usful for when you need information from a file in the project to better understand the context of the command.',
    parameters=get_project_file_contents_params
)

def get_project_file_contents(path: str) -> dict:
    """Retrieves the contents of the file at the specified path.
    
    Args:
        path (str): The path to the file.

    Returns:
        dict: A dictionary containing the content of the file and the file path.
    """
    with open(path, 'r', encoding="utf-8") as file:
        content = file.read()

        return {'path': path, 'content': content}
        
        
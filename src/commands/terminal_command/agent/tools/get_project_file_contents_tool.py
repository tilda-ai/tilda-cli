from src.lib_pkg.types.llm_tools import FunctionTool, JSONSchema

# Define the JSONSchema for 'path' property
file_path_schema = JSONSchema(
    type='string'
)

message_schema = JSONSchema(
    type='string',
    description='The reason for retrieving the file at the specified path.',
)

# Define JSONSchema for the parameters of the function
get_project_file_contents_params = JSONSchema(
    type='object',
    properties={
        'file_path': file_path_schema,
        'message': message_schema,
    },
    required=['file_path', 'message']
)

# Define the function tool using the new structure
get_project_file_contents_tool_instance = FunctionTool(
    type='function',
    function={
        'name': 'get_project_file_contents',
        'description': 'Retrieves the contents of the file at the specified path, Only use this tool if you know that a file holds information you need to generate a response.',
        'parameters': get_project_file_contents_params.to_dict()  # Convert to dictionary
    }
)

# Convert the whole function tool instance to a dictionary for serialization or further use
get_project_file_contents_tool = get_project_file_contents_tool_instance.to_dict()

# Function to get project file contents remains unchanged
def get_project_file_contents(file_path: str) -> dict:
    """Retrieves the contents of the file at the specified path.
    
    Args:
        file_path (str): The path to the file.

    Returns:
        dict: A dictionary containing the content of the file and the file path.
    """
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        return {'path': file_path, 'content': content}
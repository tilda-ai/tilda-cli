import os

def update_tildaconfig(current_directory_path: str, placeholder_pattern: str, value: str):
    config_path = os.path.join(current_directory_path, "tildaconfig.toml")
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as file:
            config_data = file.read()
        updated_config = config_data.replace(placeholder_pattern, value)
        with open(config_path, "w", encoding="utf-8") as file:
            file.write(updated_config)
            
        return {"status": "success", "message": "tildaconfig.toml updated successfully."}
    else:
        return {"status": "error", "message": "tildaconfig.toml does not exist."}

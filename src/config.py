import json
from pathlib import Path
import toml
import os
import tiktoken

from src.utils import get_project_config_files, get_tree, read_cmd_history
class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.config = toml.load("tildaconfig.toml")

    def get_config(self):
        return self.config
    
    def get_user_os(self):
        return os.name
    
    def get_project_tree(self):
        return get_tree(Path.cwd())
    
    def get_dev_env_context(self):
        return json.dumps(self.config["dev_env_context"], indent=4)

    def get_project_config_files(self):
        return get_project_config_files(Path.cwd())

    def get_working_directory(self):
        return Path.cwd()
    
    def get_commands_history(self):
        return read_cmd_history()

    def get_ollama_api_endpoint(self):
        return self.config["api_endpoints"]["ollama"]

    def get_claude_api_key(self):
        return self.config["api_keys"]["claude_api_key"]

    def get_openai_api_key(self):
        return self.config["api_keys"]["open_ai_api_key"]

    def get_gemini_api_key(self):
        return self.config["api_keys"]["gemini_api_key"]

    def get_mistral_api_key(self):
        return self.config["api_keys"]["mistral_api_key"]

    def get_groq_api_key(self):
        return self.config["api_keys"]["groq_api_key"]

    def get_terminal_tokenizer(self):
        return tiktoken.get_encoding(self.config["commands"]["terminal"]["token_encoding"])
    
    def get_terminal_command_base_model(self):
        return self.config["commands"]["terminal"]["base_model"]
    
    # TODO: Implement conversations history
    # def get_sqlite_db(self):
    #     return ".tilda/db/sqlite.db"

    # TODO: Implement dynamic configuration
    # def set_value(self, value):
    #     self.config["EXAMPLE"]["KEY"] = value
    #     self.save_config()
    
    # TODO: Implement dynamic configuration
    # def save_config(self):
    #     with open("tildaconfig.toml", "w") as f:
    #         toml.dump(self.config, f)

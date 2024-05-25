import json
from pathlib import Path
import toml
from src.lib.utils.key_handler import KeyHandler


class Config:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        current_dir = Path.cwd()
        config_path = None

        while True:
            if (current_dir / 'tildaconfig.toml').exists():
                config_path = current_dir / 'tildaconfig.toml'
                break
            parent_dir = current_dir.parent
            if parent_dir == current_dir:
                break
            current_dir = parent_dir

        if config_path is None:
            raise FileNotFoundError("tildaconfig.toml not found")

        with open(config_path, "r") as f:
            self.config = toml.load(f)

    def get_config(self):
        return self.config
    
    def get_dev_env_context(self):
        return json.dumps(self.config["dev_env_context"], indent=4)

    def get_llm_api_key(self):
        return KeyHandler.get_key(self.get_llm_api_key_name())
    
    def get_llm_api_key_name(self):
        return 'openai_api_key'
    
    def get_terminal_command_base_model(self):
        return self.config["commands"]["terminal"]["base_model"]
    
    def get_terminal_command_mock_response(self):
        return self.config["commands"]["terminal"]["mock_response"]
    
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

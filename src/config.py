import json
from venv import logger
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
        self.config = toml.load("tildaconfig.toml")

    def get_config(self):
        return self.config
    
    def get_dev_env_context(self):
        return json.dumps(self.config["dev_env_context"], indent=4)

    def get_llm_api_key(self):
        logger.info("Getting OpenAI API key")
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

import toml
import os
import tiktoken

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        # If the config file doesn't exist, copy from the sample
        if not os.path.exists("tildaconfig.toml"):
            with open("tildaconfig.sample.toml", "r") as f_in, open("tildaconfig.toml", "w") as f_out:
                f_out.write(f_in.read())

        self.config = toml.load("tildaconfig.toml")

    def get_config(self):
        return self.config
    
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

    def get_sqlite_db(self):
        return self.config["storage"]["sqlite_db"]

    def get_terminal_tokenizer(self):
        return tiktoken.get_encoding(self.config["commands"]["terminal"]["token_encoding"])
    
    def get_terminal_base_model(self):
        return self.config["commands"]["terminal"]["base_model"]
    
    # def set_value(self, value):
    #     self.config["EXAMPLE"]["KEY"] = value
    #     self.save_config()

    def save_config(self):
        with open("tildaconfig.toml", "w") as f:
            toml.dump(self.config, f)

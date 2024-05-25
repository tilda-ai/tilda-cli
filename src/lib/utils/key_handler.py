import os
from pathlib import Path
import toml
import keyring

class KeyHandler:

    @staticmethod
    def load_config():
        try:
            current_directory_path = Path.cwd()
            config_path = os.path.join(current_directory_path, "tildaconfig.toml")
            return toml.load(config_path)
        except Exception as e:
            raise FileNotFoundError(f"Unable to load the config file: {config_path}") from e

    @staticmethod
    def get_service_name():
        config = KeyHandler.load_config()
        try:
            return config["service_config"]["service_name"]
        except KeyError:
            raise KeyError("Service name not found in the configuration.")

    @staticmethod
    def set_key(key_name, key_value):
        """Stores a key in the system's keychain, distinctly marked as a key."""
        service_name = KeyHandler.get_service_name()
        keyring.set_password(service_name, f'_key_{key_name}', key_value)

    @staticmethod
    def get_key(key_name):
        """Retrieves a key from the system's keychain, distinctly marked as a key."""
        service_name = KeyHandler.get_service_name()
        return keyring.get_password(service_name, f'_key_{key_name}')

    @staticmethod
    def delete_key(key_name):
        """Deletes a key from the system's keychain, distinctly marked as a key."""
        service_name = KeyHandler.get_service_name()
        keyring.delete_password(service_name, f'_key_{key_name}')

import os
from src.logger import logger
from src.utils import get_jinja_env


def touch_tildaconfig(base_path: str):
    config_path = os.path.join(base_path, "tildaconfig.toml")
    if not os.path.exists(config_path):
        env = get_jinja_env()

        sample_config = env.get_template('init/tildaconfig.jinja2').render()
        # save the sample config to tildaconfig.toml
        with open(config_path, "w", encoding="utf-8") as file:

            file.write(sample_config)
        logger.info("tildaconfig.toml created successfully.")
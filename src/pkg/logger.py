import logging
from src.pkg.types.singleton_meta import SingletonMeta

#TODO: implement dymamic logger name
# gpt-conversation: https://chat.openai.com/share/79071939-4f59-4e30-a0e9-b3efedbcb0af
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    parser = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + parser + reset,
        logging.INFO: grey + parser + reset,
        logging.WARNING: yellow + parser + reset,
        logging.ERROR: red + parser + reset,
        logging.CRITICAL: bold_red + parser + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

class Logger(metaclass=SingletonMeta):
    def __init__(self):
        self.logger = logging.getLogger("tilda")
        self.logger.setLevel(logging.NOTSET)
        ch = logging.StreamHandler()
        ch.setLevel(logging.NOTSET)
        ch.setFormatter(CustomFormatter())
        self.logger.addHandler(ch)

    def get_logger(self):
        return self.logger


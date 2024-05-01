import logging

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

logger = logging.getLogger("tilda")
logger.setLevel(logging.NOTSET)

ch = logging.StreamHandler()
ch.setLevel(logging.NOTSET)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)

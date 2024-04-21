import logging
import os


def append_to_file(filename, entry):
    if os.path.exists(filename):
        with open(filename, 'r+') as file:
            content = file.read()
            if entry in content:
                logging.info(f"{entry} is already listed in {filename}.")
            else:
                file.write(f"\n\n{entry}")
                logging.info(f"{entry} added to {filename} successfully.")
    else:
        logging.info(f"Could not find {filename}. Make sure you DO NOT publish your {entry} file to a public repository without reducting it's content from sensitive information.")

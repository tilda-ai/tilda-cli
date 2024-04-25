#!/usr/bin/env python3

import logging

from .config import Config

# Set up default logging for the entire package
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

config = Config()


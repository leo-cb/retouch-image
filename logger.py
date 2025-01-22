"""Creates a logger"""

import sys
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create a stream handler to output log messages to stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)

# Create a file handler to output log messages to a file
file_handler = logging.FileHandler('log.log')
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for both handlers
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the stream handler and file handler to the logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

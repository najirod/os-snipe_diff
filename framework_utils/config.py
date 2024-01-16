import sys
import logging
from datetime import date
import os


def get_root_path():
    # This function retrieves the root path of the application.
    if "venv" in sys.path[0]:
        root_path = (sys.path[1] + "/")  # Use the second item in sys.path as the root path.
    else:
        root_path = (sys.path[0] + "/")  # Use the first item in sys.path as the root path.
    return root_path


def configure_logging(log_file_name, logger_name):
    """
    Configures and sets up logging for the application.

    Args:
        log_file_name (str): The name of the log file.
        logger_name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger object.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # Ensure the "logs" directory exists.

    log_file_path = os.path.join(log_dir, log_file_name)  # Create the full log file path.

    logger = logging.getLogger(logger_name)  # Create a logger object with the specified name.

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)  # Set the logger's level to capture DEBUG and higher-level messages.
        formatter = logging.Formatter(
            '%(asctime)s:%(pathname)s:%(funcName)s:%(name)s:%(process)d - %(levelname)s -: %(message)s')

        file_handler = logging.FileHandler(log_file_path)  # Create a file handler to write log messages to the file.
        file_handler.setFormatter(formatter)  # Set the formatter for the file handler.

        stream_handler = logging.StreamHandler()  # Create a stream handler to display log messages on the console.
        stream_handler.setFormatter(formatter)  # Set the formatter for the stream handler.

        logger.addHandler(file_handler)  # Add the file handler to the logger.
        logger.addHandler(stream_handler)  # Add the stream handler to the logger.

    return logger  # Return the configured logger object.

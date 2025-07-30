# logger_config.py

import logging
import os

def setup_logger(name="ipl_logger", log_file="ipl_project.log", level=logging.DEBUG):
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", log_file)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger

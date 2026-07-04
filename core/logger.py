import logging
import sys

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate handlers if the logger is already initialized
    if not logger.handlers:
        # Define standard enterprise log format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # StreamHandler to forward logs to terminal standard output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        # FileHandler to persist security audit trails locally
        file_handler = logging.FileHandler("app.log", encoding="utf-8")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
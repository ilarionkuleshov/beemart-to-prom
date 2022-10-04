import logging


def get_logger(logs_file_path):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler(logs_file_path),
            logging.StreamHandler()
        ]
    )
    logger = logging.getLogger()
    return logger

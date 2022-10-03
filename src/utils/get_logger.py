import logging


def get_logger(logs_file_path):
    logger = logging.getLogger(__name__)

    log_formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(log_formatter)

    file_handler = logging.FileHandler(logs_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger

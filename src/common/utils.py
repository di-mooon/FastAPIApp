import logging

_log_format = "%(asctime)s [%(levelname)s] %(message)s"


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler


def init_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(get_stream_handler())

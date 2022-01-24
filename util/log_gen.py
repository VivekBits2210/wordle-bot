import logging


def get_logger(name):
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s %(module)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %z",
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger

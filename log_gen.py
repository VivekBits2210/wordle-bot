import logging

def get_logger(name):
    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s %(module)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S %Z"
    )
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger
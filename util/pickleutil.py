import os
import pickle
from util.log_gen import get_logger

logger = get_logger(__file__)


def pull_pickle_file(pickle_file_path):
    try:
        if os.path.exists(pickle_file_path):
            with open(pickle_file_path, "rb") as f:
                data = pickle.load(f)
            return data
    except KeyError:
        logger.error(f"Pickle file {pickle_file_path} has invalid structure")
    except pickle.PicklingError:
        logger.error(
            f"Failed to load pickle file {pickle_file_path}, probably corrupted."
        )
    return None


def push_pickle_file(pickle_file_path, data):
    try:
        with open(pickle_file_path, "wb") as f:
            pickle.dump(data, f)
    except pickle.PicklingError:
        logger.error(f"Failed to push to pickle file {pickle_file_path}")

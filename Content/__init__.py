import os


def get_path() -> str:
    return os.path.dirname(os.path.realpath(__file__))

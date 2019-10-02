from os import mkdir
from os.path import exists, abspath


def find_or_create(directory: str):
    abs_path = abspath(directory)

    if not exists(abs_path):
        mkdir(abs_path)

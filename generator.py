from request import Request
from extenders import double_normal_distribution
from os import path, makedirs

if __name__ == "__main__":
    if not path.exists("./test_data"):
        makedirs("./test_data")
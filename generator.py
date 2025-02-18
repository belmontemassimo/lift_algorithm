from request import Request
from extenders import double_normal_distribution
from os import path, makedirs

max_floor: int = 20
min_floor: int = 0

if __name__ == "__main__":
    if not path.exists("./test_data"):
        makedirs("./test_data")


def request_to_dict(request: Request):
    request_dict: dict = {}
    request_dict["request_floor"] = request.request_floor
    request_dict["target_floor"] = request.target_floor
    request_dict["time_created"] = request.time_created
    request_dict["weight_captor"] = request.weight_captor

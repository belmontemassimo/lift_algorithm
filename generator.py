from request import Request
from extenders import double_normal_distribution
from os import path, makedirs
from random import randint

if __name__ == "__main__":
    if not path.exists("./test_data"):
        makedirs("./test_data")
    requests: list[Request] = []
    max_floor: int = int(input("max_floor: "))
    min_floor: int = int(input("min_floor: "))
    num_requests: int = int(input("num_requests: "))
    total_time: int = int(input("total_time: "))

    for _ in range(num_requests):
        request_floor = randint(min_floor,max_floor)
        target_floor = randint(min_floor,max_floor)
        created_time = randint(0,total_time)
        weight = int(double_normal_distribution() * 100)
        requests.append(Request(request_floor, target_floor, created_time, weight))


def request_to_dict(request: Request):
    request_dict: dict = {}
    request_dict["request_floor"] = request.request_floor
    request_dict["target_floor"] = request.target_floor
    request_dict["time_created"] = request.time_created
    request_dict["weight_captor"] = request.weight_captor

from request import Request
from extenders import double_normal_distribution
from os import path, makedirs
from random import randint
from os import listdir
from json import dump, loads

if __name__ == "__main__":
    if not path.exists("./samples"):
        makedirs("./samples")
    requests: list[dict[str,int]] = []
    max_floor: int = int(input("max_floor: "))
    num_requests: int = int(input("num_requests: "))
    total_time: int = int(input("total_time: "))
    if max_floor <= 1 or num_requests <= 0 or total_time <= 0:
        print("incorrect inputs")
        exit()

    while True:
        request_floor = randint(0,max_floor)
        target_floor = randint(0,max_floor)
        created_time = randint(0,total_time)
        weight_captor = int(double_normal_distribution() * 100)
        if request_floor != target_floor:
            requests.append({"request_floor": request_floor, "target_floor": target_floor, "created_time": created_time, "weight_captor": weight_captor})
            if len(requests) == num_requests-1:
                break
    all_samples = listdir("./samples")

    sample_number = 1
    while True:
        if f"sample_{sample_number}" in all_samples:
            sample_number += 1
            continue
        with open(f"./samples/sample_{sample_number}", "w") as file:
            dump(requests, file)
            break
    print(f"saved as sample_{sample_number}")

def dict_to_request(request_dict: dict[str,int]):
    return Request(request_dict["request_floor"], request_dict["target_floor"], request_dict["time_created"], request_dict["weight_captor"])

def samples_list() -> list[str]:
    return listdir("./samples")

def load_sample(file_name: str) -> list[Request]:
    with open(f"./samples/{file_name}", "r") as file:
        return [dict_to_request({key: value for key, value  in request_dict.iteritems()}) for request_dict in loads(file.read())]

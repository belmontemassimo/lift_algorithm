from enum import Enum
from extenders import double_normal_distribution

# 
class Direction(Enum):
    UP = 1
    DOWN = -1

class Request:
    def __init__(self, request_floor:int , target_floor: int, time_created: float):
        self.request_floor = request_floor
        self.target_floor = target_floor
        self.time_created = time_created
        self.direction = Direction.UP if (request_floor-target_floor) < 0 else Direction.DOWN
        self.weight_captor = int(double_normal_distribution(mean=70, std_dev=12.5, second_mean=3.5, second_std_dev=0.5)*100)


    def waiting_time(self, current_time: float) -> float:
        return current_time - self.time_created
    


    # compares the waited times
    def __lt__(self, other_request: float):
        # if other is not a Request object, return NotImplemented
        if not isinstance(other_request, Request):
            return NotImplemented
        return self.waiting_time() < other_request.waiting_time()
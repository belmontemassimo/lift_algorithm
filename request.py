from enum import Enum
from extenders import double_normal_distribution
 
class Direction(Enum):
    UP = 1
    DOWN = -1

class Request:
    request_floor: int
    target_floor: int
    time_created: float    
    time_on_floor: float
    time_in_lift: float
    weight_captor: int
    direction: Direction

    def __init__(self, request_floor:int , target_floor: int, time_created: float, weight_captor: int = 0):
        self.request_floor = request_floor
        self.target_floor = target_floor
        self.time_created = time_created
        self.direction = Direction.UP if (request_floor-target_floor) < 0 else Direction.DOWN
        if weight_captor != 0:
            self.weight_captor = weight_captor * 100
        else:
            self.weight_captor = int(double_normal_distribution(mean=70, std_dev=12.5, second_mean=3.5, second_std_dev=0.5)*100)


    def waiting_time(self, current_time: float) -> float:
        return current_time - self.time_created
    
    def lift_check_in(self, time: float):
        self.time_on_floor = time - self.time_created
        return True
    
    def floor_check_in(self, time: float):
        self.time_in_lift = time - self.time_on_floor
        return True

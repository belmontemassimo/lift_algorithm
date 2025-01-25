from enum import Enum
import time

class LiftStatus(Enum):
    IDLE = 0
    MOVING = 1
    WAITING = 2

class DeltaTime:
    previous_time: float

    def __init__(self):
        self.previous_time = time.time()

    def __call__(self) -> float:
        cur_time = time.time()
        deltatime = cur_time - self.previous_time
        self.previous_time = cur_time
        return deltatime
    
def Interpolate(current: float, change_rate: float, deltatime: float) -> float:
    return current + change_rate * deltatime

def InterpolateTo(current: float, change_rate: float, deltatime: float, to: float) -> float:
    if current < to:
        current = min(current + change_rate * deltatime, to)
    elif current > to:
        current = max(current - change_rate * deltatime, to)
    return current
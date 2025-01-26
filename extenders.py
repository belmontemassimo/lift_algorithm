#
#   This is a module for having some useful, generalised and obstructed code that can be used by any other module.
#

import time

# function to return the time difference between now and the last time it was called
class DeltaTime:
    previous_time: float

    def __init__(self):
        self.previous_time = time.time()

    def __call__(self) -> float:
        cur_time = time.time()
        deltatime = cur_time - self.previous_time
        self.previous_time = cur_time
        return deltatime
    
# function to change value by sertain number of units per second based on time passed
# current: value to change
# change_rate: units per second
# deltatime: time passed since last update
def Interpolate(current: float, change_rate: float, deltatime: float) -> float:
    return current + change_rate * deltatime

# same as interpolate function but with a target value aka to
# this function may have some flactuations in return when near the target value
def InterpolateTo(current: float, change_rate: float, deltatime: float, to: float) -> float:
    if current < to:
        current = min(Interpolate(current, change_rate, deltatime), to)
    elif current > to:
        current = max(Interpolate(current, -change_rate, deltatime), to)
    return current
#
#   This is a module for having some useful, generalised and obstructed code that can be used by any other module.
#

import time

# global variables for this file
time_multiplier = 1

def set_time_multiplier(time_multiplier_incoming):
    global time_multiplier
    time_multiplier = time_multiplier_incoming

# function to return the time difference between now and the last time it was called
class DeltaTime:
    previous_time: float
    time_multiplier: float

    def __init__(self):
        global time_multiplier
        self.previous_time = 0.0
        self.time_multiplier = time_multiplier

    def __call__(self) -> float:
        if self.previous_time == 0.0:
            self.previous_time = time.time()
            return 0.0
        cur_time = time.time()
        deltatime = (cur_time - self.previous_time) * self.time_multiplier
        self.previous_time = cur_time
        return deltatime
    
# function to change value by certain number of units per second based on time passed
# current: value to change (speed, acceleration)
# change_rate: units per second
# deltatime: time passed since last update
def Interpolate(current: float, change_rate: float, deltatime: float) -> float:
    return current + change_rate * deltatime

# same as interpolate function but with a target value aka to
# this function may have some fluctuations in return when near the target value
def InterpolateTo(current: float, change_rate: float, deltatime: float, expected_value: float, only_soft_catch: bool = False) -> float:
    if current < expected_value:
        current = Interpolate(current, change_rate, deltatime)
        if (current > expected_value) and (not only_soft_catch or change_rate <= 0.05):
            return expected_value
    if current > expected_value:
        current = Interpolate(current, change_rate, deltatime)
        if (current < expected_value) and (not only_soft_catch or change_rate <= 0.05):
            return expected_value
    return current
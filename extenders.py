#
#   This is a module for having some useful, generalised and obstructed code that can be used by any other module.
#
from random import gauss
from time import time

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
            self.previous_time = time()
            return 0.0
        cur_time = time()
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
        if (current > expected_value) and (not only_soft_catch or abs(change_rate) <= 0.1):
            return expected_value
    if current > expected_value:
        current = Interpolate(current, change_rate, deltatime)
        if (current < expected_value) and (not only_soft_catch or abs(change_rate) <= 0.1):
            return expected_value
    return current

# Generate a person's weight following a normal distribution.
def double_normal_distribution(mean: float = 70, std_dev: float = 12.5, second_mean: float = 3.5, second_std_dev: float = 0.5) -> float:
    return max(30, gauss(mean, std_dev)) + max(0, gauss(second_mean, second_std_dev))  # Minimum weight of 30kg to avoid unrealistic values

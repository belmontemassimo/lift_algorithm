import time
from enum import Enum
from extenders import DeltaTime, InterpolateTo

# used to ensure that the lift state is consistent
# subject to change
class LiftState(Enum):
    IDLE = 0
    MOVING = 1
    WAITING = 2

# class to represent a lift
class Lift:
    position: float = 0
    speed: float = 0
    deltatime: DeltaTime
    acceleration: float = 0
    max_speed: float = 0
    capacity: int = 0
    target_floor: float = 0
    status: LiftState

    # init function with default values for lift
    def __init__(self, capacity: int, max_speed: float, acceleration: float, time_multiplier: float = 1):
        self.deltatime = DeltaTime(time_multiplier)
        self.status = LiftState.IDLE
        self.previous_time = time.time()
        self.capacity = capacity
        self.max_speed = max_speed
        self.acceleration = acceleration

    # function to update the lift's position and speed
    # should be run frequently to ensure accuracy 
    def update(self):
        deltatime = self.deltatime()
        stopping_distance = self.speed ** 2 / (2 * self.acceleration)
        speed = InterpolateTo(self.speed, self.acceleration, deltatime, self.max_speed)
        position = InterpolateTo(self.position, speed, deltatime, self.target_floor)
        if abs(position - self.target_floor) < stopping_distance:
            speed = InterpolateTo(self.speed, self.acceleration, deltatime, 0)
            position = InterpolateTo(self.position, speed, deltatime, self.target_floor)
        self.speed = speed
        self.position = position
        
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
    target_floor: list[float]
    status: LiftState

    # note: target_floor is a lift with ONLY ONE value (so far) because lists are passed by reference
    # so it can be changed from outside the class without calling any class functions 
    def __init__(self, capacity: int, max_speed: float, acceleration: float, target_floor: list[float]):
        self.deltatime = DeltaTime()
        self.status = LiftState.IDLE
        self.previous_time = time.time()
        self.capacity = capacity
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.target_floor = target_floor

    # function to update the lift's position and speed
    # should be run frequently to ensure accuracy 
    def update(self):
        deltatime = self.deltatime()
        stopping_distance = self.speed ** 2 / (2 * self.acceleration)
        speed = InterpolateTo(self.speed, self.acceleration, deltatime, self.max_speed)
        position = InterpolateTo(self.position, speed, deltatime, self.target_floor[0])
        if abs(position - self.target_floor[0]) < stopping_distance:
            speed = InterpolateTo(self.speed, self.acceleration, deltatime, 0)
            position = InterpolateTo(self.position, speed, deltatime, self.target_floor[0])
        self.speed = speed
        self.position = position
        
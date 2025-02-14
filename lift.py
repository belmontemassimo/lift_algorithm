from enum import Enum
from extenders import DeltaTime, InterpolateTo
from math import copysign
from request import Request

# used to ensure that the lift state is consistent
# subject to change
class LiftState(Enum):
    IDLE = 0
    MOVING = 1
    WAITING = 2
    AFTERWAIT = 3

# class to represent a lift
class Lift:
    position: float = 0
    speed: float = 0
    deltatime: DeltaTime
    acceleration: float = 0
    max_speed: float = 0
    weight: float = 0
    waiting_time: float = 0
    waited_time: float = 0
    capacity: int = 0
    picked_requests: list[Request]
    target_floor: float = 0
    state: LiftState

    # init function with default values for lift
    def __init__(self, capacity: int, max_speed: float, acceleration: float, waiting_time):
        self.deltatime = DeltaTime()
        self.state = LiftState.IDLE
        self.capacity = capacity * 100
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.waiting_time = waiting_time
        self.picked_requests = []

    def move(self, deltatime: float):
        stopping_distance = self.speed ** 2 / (2 * abs(self.acceleration))

        # if the lift goes above the target floor, reverse the speed and the acceleration until it reaches the target floor
        if self.position > self.target_floor and self.acceleration > 0:
            self.max_speed = -self.max_speed
            self.acceleration = -self.acceleration
        # if the lift goes below the target floor, reverse the speed and the acceleration until it reaches the target floor
        elif self.position < self.target_floor and self.acceleration < 0:
            self.max_speed = -self.max_speed
            self.acceleration = -self.acceleration
        # update speed so that it reaches the max_speed and the position in case it went above the target_floor
        speed = InterpolateTo(self.speed, self.acceleration, deltatime, self.max_speed)
        position = InterpolateTo(self.position, speed, deltatime, self.target_floor, True, 9)
        # if the lift is within the stopping distance, decelerate
        if abs(position - self.target_floor) <= stopping_distance and copysign(1, self.speed) == copysign(1, self.target_floor - self.position):
            speed = InterpolateTo(self.speed, -self.acceleration, deltatime, 0)
            position = InterpolateTo(self.position, speed, deltatime, self.target_floor, True, 9)
        self.speed = speed
        self.position = position

    def add_request(self, request: Request) -> bool:

        if self.weight + request.weight_captor <= self.capacity:
            self.picked_requests.append(request)
            self.weight += request.weight_captor
            return True
        else:
            return False
        
    def remove_request(self, request: Request) -> bool:
        if request in self.picked_requests:
            self.picked_requests.remove(request)
            self.weight -= request.weight_captor
            return True

    # function to update the lift's position and speed
    # should be run frequently to ensure accuracy 
    def update(self):
        deltatime = self.deltatime()
        match self.state:
            case LiftState.IDLE:
                self.move(deltatime)
                if self.position == self.target_floor and abs(self.speed) <= 0.1:
                    self.speed = 0
            case LiftState.MOVING:
                self.move(deltatime)
                if self.position == self.target_floor and abs(self.speed) <= 0.1:
                    self.state = LiftState.WAITING
                    self.speed = 0
            case LiftState.WAITING:
                self.waited_time += deltatime
                if self.waited_time >= self.waiting_time:
                    self.state = LiftState.AFTERWAIT
                    self.waited_time = 0
 
        
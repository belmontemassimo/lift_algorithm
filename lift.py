from enum import Enum
from extenders import DeltaTime, InterpolateTo
from math import copysign
from request import Request

# used to ensure that the lift state is consistent
class LiftState(Enum):
    IDLE = 0
    MOVING = 1
    WAITING = 2
    AFTERWAIT = 3

# class to represent a lift
class Lift:
    # variable definition
    position: float = 0
    speed: float = 0
    deltatime: DeltaTime
    acceleration: float = 0
    max_speed: float = 0
    weight: int = 0
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
        self.capacity = capacity * 100 # (* 100) as passed as kg but stored as 10g to avoid float inaccuracy
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.waiting_time = waiting_time
        self.picked_requests = []

    # performs calculations to determine next position of a lift 
    def move(self, deltatime: float):
        # determines required distance to stop form speed and acceleration
        stopping_distance = self.speed ** 2 / (2 * abs(self.acceleration))

        # if the lift goes above the target floor, reverse the speed and the acceleration until it reaches the target floor (only if overshoot)
        if self.position > self.target_floor and self.acceleration > 0:
            self.max_speed = -self.max_speed
            self.acceleration = -self.acceleration
        # if the lift goes below the target floor, reverse the speed and the acceleration until it reaches the target floor (only if overshoot)
        elif self.position < self.target_floor and self.acceleration < 0:
            self.max_speed = -self.max_speed
            self.acceleration = -self.acceleration
        # update speed and position by interpolating
        speed = InterpolateTo(self.speed, self.acceleration, deltatime, self.max_speed)
        position = InterpolateTo(self.position, speed, deltatime, self.target_floor, only_soft_catch=True) # only_soft_catch, overshoot if too fast
        # if the lift is within the stopping distance, decelerate
        if abs(position - self.target_floor) <= stopping_distance and copysign(1, self.speed) == copysign(1, self.target_floor - self.position):
            # update speed and position with inverted acceleration 
            speed = InterpolateTo(self.speed, -self.acceleration, deltatime, 0)
            position = InterpolateTo(self.position, speed, deltatime, self.target_floor, True)
        # save final speed and position
        self.speed = speed
        self.position = position
    
    # add request if it can be added
    def add_request(self, request: Request) -> bool:

        # add request if weight would not exceed capacity
        if self.weight + request.weight_captor <= self.capacity:
            self.picked_requests.append(request)
            self.weight += request.weight_captor
            return True
        else:
            return False
        
    # remove request if carried by this lift
    def remove_request(self, request: Request) -> bool:
        if request in self.picked_requests:
            self.picked_requests.remove(request)
            self.weight -= request.weight_captor
            return True
        return False

    # updates states, position and speed 
    def update(self):
        deltatime = self.deltatime() # time passed from the last time called 
        match self.state:

            # move lift, stop if reaches target floor slow enough in idle mode
            case LiftState.IDLE:
                self.move(deltatime)
                if round(self.position, 5) == self.target_floor and abs(self.speed) <= 0.1:
                    self.speed = 0
                    self.position = self.target_floor

            # move lift, stop and go to waiting mode if reaches target floor slow enough 
            case LiftState.MOVING:
                self.move(deltatime)
                if round(self.position, 5) == self.target_floor and abs(self.speed) <= 0.1:
                    self.state = LiftState.WAITING
                    self.speed = 0
                    self.position = self.target_floor
            # wait for a certain amount of time then proceed to afterwait mode to request new target floor
            case LiftState.WAITING:
                self.waited_time += deltatime
                if self.waited_time >= self.waiting_time:
                    self.state = LiftState.AFTERWAIT
                    self.waited_time = 0
 
        

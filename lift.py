import time
from extenders import LiftStatus, DeltaTime, InterpolateTo

class Lift:
    position: float = 0
    speed: float = 0
    deltatime = DeltaTime()
    acceleration: float = 0
    max_speed: float = 0
    capacity: int = 0
    target_floor: int = 0
    status = LiftStatus.IDLE


    def __init__(self, capacity: int, max_speed: float, acceleration: float):
        self.previous_time = time.time()
        self.capacity = capacity
        self.max_speed = max_speed
        self.acceleration = acceleration

    def move_to(self, target_floor: int):
        self.target_floor = target_floor

    # LOOPED FROM SIMULATION !!!!!!
    def update(self):
        deltatime = self.deltatime()
        stopping_distance = self.speed ** 2 / (2 * self.acceleration)
        if abs(self.position - self.target_floor) < stopping_distance:
            self.speed = InterpolateTo(self.speed, self.acceleration, deltatime, 0)
        else:
            self.speed = InterpolateTo(self.speed, self.acceleration, deltatime, self.max_speed)
        self.position = InterpolateTo(self.position, self.speed, deltatime, self.target_floor)

        

        
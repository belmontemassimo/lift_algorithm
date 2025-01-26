from lift import Lift
import time
import threading

class LiftManager:
    num_floors: int
    num_lifts: int
    lifts: list[Lift]
    lifts_thread: threading.Thread

    def __init__(self, num_floors, num_lifts, max_speed, acceleration, capacity):
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.target_floors = [[0] for _ in range(num_lifts)]
        self.lifts = [Lift(capacity, max_speed, acceleration, self.target_floors[i]) for i in range(num_lifts)]
        self.lifts_thread = threading.Thread(target=lifts_update_circle, args=(self.lifts,))
        self.lifts_thread.start()

    def lifts_positions(self):
        return [lift.position for lift in self.lifts]

def lifts_update_circle(lifts: list[Lift]):
    while True:
        for lift in lifts:
            lift.update()
        time.sleep(0.001)
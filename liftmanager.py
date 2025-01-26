from lift import Lift
import time
import threading

# class to manage multiple lifts
# ensures easy flow of information between lifts
class LiftManager:
    num_floors: int
    num_lifts: int
    lifts: list[Lift]
    lifts_thread: threading.Thread

    # craete and set lifts 
    # capacity: max weight in kg
    def __init__(self, num_floors, num_lifts, max_speed, acceleration, capacity):
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.target_floors = [[0] for _ in range(num_lifts)]
        self.lifts = [Lift(capacity, max_speed, acceleration, self.target_floors[i]) for i in range(num_lifts)]
        # this part launches a thread to update lifts in a more predictable way (semi temporary)
        self.lifts_thread = threading.Thread(target=lifts_update_circle, args=(self.lifts,))
        self.lifts_thread.start()

    # returns lift of all lifts opsitions
    def lifts_positions(self):
        return [lift.position for lift in self.lifts]

# semi temporary function to provide at least some level of consistency for lift updates
def lifts_update_circle(lifts: list[Lift]):
    while True:
        for lift in lifts:
            lift.update()
        time.sleep(0.001)
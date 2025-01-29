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

    # create and set lifts 
    # capacity: max weight in kg
    def __init__(self, num_floors, num_lifts, max_speed, acceleration, capacity, waiting_time):
        self.num_floors = num_floors
        self.num_lifts = num_lifts
        self.lifts = [Lift(capacity, max_speed, acceleration, waiting_time) for i in range(num_lifts)]
        # this part launches a thread to update lifts in a more predictable way (semi temporary)
        self.lifts_thread = threading.Thread(target=lifts_update_circle, args=(self.lifts,))
        self.lifts_thread.start()

    # returns lift of all lifts opsitions
    def get_positions(self):
        return [lift.position for lift in self.lifts]
    
    def get_speed(self):
        return [lift.speed for lift in self.lifts]
    
    # return target floor for all lifts
    def get_target_floors(self):
        return [lift.target_floor for lift in self.lifts]
    
    def get_states(self):
        return [lift.state for lift in self.lifts]
    
    def set_lifts_states(self, states):
        for i, state in enumerate(states):
            self.lifts[i].state = state
    
    # set target floor for all lifts
    def set_target_floors(self, target_floors):
        for i, target_floor in enumerate(target_floors):
            self.lifts[i].target_floor = target_floor

    # semi temporary function to provide at least some level of consistency for lift updates
    def run_updates(self):
        while True:
            for lift in self.lifts:
                lift.update()
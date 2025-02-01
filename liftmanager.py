from lift import Lift

# class to manage multiple lifts
# ensures easy flow of information between lifts
class LiftManager:
    num_lifts: int
    num_floors: int
    lifts: list[Lift]
    capacity: float

    # create and set lifts 
    # capacity: max weight in kg
    def __init__(self, num_floors, num_lifts, max_speed, acceleration, capacity, waiting_time,q):
        self.num_lifts = num_lifts
        self.num_floors = num_floors
        self.capacity = capacity
        self.lifts = [Lift(capacity, max_speed, acceleration, waiting_time,q) for i in range(num_lifts)]

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
    
    def set_states(self, states):
        for i, state in enumerate(states):
            self.lifts[i].state = state

    def get_weight(self):
        return [lift.weight for lift in self.lifts]
    
    def get_weight_kg(self):
        return [lift.weight/100 for lift in self.lifts]
    
    # set target floor for all lifts
    def set_target_floors(self, target_floors):
        for i, target_floor in enumerate(target_floors):
            self.lifts[i].target_floor = target_floor

    # semi temporary function to provide at least some level of consistency for lift updates
    def run_updates(self):
        for lift in self.lifts:
            lift.update()
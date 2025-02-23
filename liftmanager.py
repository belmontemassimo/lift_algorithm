from lift import Lift

# class to manage multiple lifts
# ensures easy flow of information in and out of lifts
class LiftManager:
    # variable definition
    num_lifts: int
    num_floors: int
    lifts: list[Lift]
    capacity: float

    # init unconfigured lifrt manager
    def __init__(self) -> None:
        self.lifts = []
        self.capacity = 0
        self.num_floors = 0
        self.num_lifts = 0
    
    # configure lift manager
    def configure(self, num_floors: int, num_lifts: int, max_speed: float, acceleration: float, capacity: int, waiting_time: float):
        self.num_lifts = num_lifts
        self.num_floors = num_floors
        self.capacity = capacity
        # init list of all lifts
        self.lifts = [Lift(capacity, max_speed, acceleration, waiting_time) for _ in range(num_lifts)]

    # returns position of all lifts
    def get_positions(self):
        return [lift.position for lift in self.lifts]
    
    # returns speed of all lifts
    def get_speed(self):
        return [lift.speed for lift in self.lifts]
    
    # return target floor for all lifts
    def get_target_floors(self):
        return [lift.target_floor for lift in self.lifts]
    # returns state of all lifts
    def get_states(self):
        return [lift.state for lift in self.lifts]
    
    # set state of every single lift
    def set_states(self, states):
        for i, state in enumerate(states):
            self.lifts[i].state = state
    
    # get weight that is in every lift (1 = 10g)
    def get_weight(self):
        return [lift.weight for lift in self.lifts]
    
    # get weight in kilograms that is in every lift (1 = 1kg)
    def get_weight_kg(self):
        return [lift.weight/100 for lift in self.lifts]
    
    # set target floor for all lifts
    def set_target_floors(self, target_floors):
        for i, target_floor in enumerate(target_floors):
            self.lifts[i].target_floor = target_floor

    # runs update loop for every single lift 
    def run_updates(self):
        for lift in self.lifts:
            lift.update()

from request import Request, Direction
from lift import Lift, LiftState
from liftmanager import LiftManager
from inspect import getmembers, isclass
from importlib import import_module
import math

# get the name of the algorithms listed in the algorithms.py file and returns a dictionary conatining the name as key and the class as value
def get_algorithms() -> dict[str,object]:
    module = import_module("algorithms")
    return {algorithm_name: algorithm_class for algorithm_name, algorithm_class in getmembers(module, isclass) if algorithm_class.__module__ == module.__name__ and algorithm_name != "AlgorithmHandler"}

class AlgorithmHandler:
    algorithm: object
    algorithms: dict[str,object]

    def __init__(self):
        self.algorithm = FCFS()
        self.algorithms = get_algorithms()

    # returns the next floor to move to and the lift status
    def __call__(self, lift_manager: LiftManager, current_requests: list[Request]):
        #TEMP
        match self.algorithm:
            case FCFS() | SCAN() | LOOK() | MYLIFT():
                return [self.algorithm(lift, current_requests) for lift in lift_manager.lifts]
            case _:
                return self.algorithm(lift_manager, current_requests)
            
    
    # returns the list of algorithms names
    def get_list(self) -> dict[str,object]:
        return list(self.algorithms.keys())
    
    # allows the user to change algorithm in use
    def set_algorithm(self, algorithm_name: str):
        self.algorithm = self.algorithms[algorithm_name]()

# create algorithm class for each algorithm
class FCFS:
    def __call__(self, lift: Lift, current_requests: list[Request]) -> float | None:
        picked_requests = lift.picked_requests
        if picked_requests:
            return picked_requests[0].target_floor
        
        if current_requests:
            return current_requests[0].request_floor
        
        return None


class SCAN:
    def __call__(self, lift: Lift, current_requests: list[Request]) -> float | None:
        picked_requests = lift.picked_requests
        if not current_requests and not picked_requests:
            return None # No requests, lift remains idle
        
        if lift.state == LiftState.IDLE:
            return min(current_requests, key=lambda request: abs(request.request_floor - lift.position)).request_floor

        # Collect all requested floors
        all_requests = [req.target_floor for req in picked_requests] + [req.request_floor for req in current_requests]
        all_requests = sorted(set(all_requests))  # Remove duplicates and sort
            
        # Determine scan direction based on the closest request
        up_requests = [floor for floor in all_requests if floor > lift.position]
        down_requests = [floor for floor in all_requests if floor < lift.position]

        if up_requests:
            return up_requests[0]  # Move to the next highest request first
        elif down_requests:
            return down_requests[-1] # Move to the lowest request if no higher requests remain
        return None

class LOOK:
    direction = Direction.UP

    def __call__(self, lift: Lift, current_requests: list[Request]) -> float | None:
        picked_requests = lift.picked_requests
        
        if not picked_requests and not current_requests:
            return None  # No requests, lift remains idle

        sorted_picked = sorted(picked_requests, key=lambda request: request.target_floor)

        all_requests = []

        if lift.state == LiftState.IDLE:
            return min(current_requests, key=lambda request: abs(request.request_floor - lift.position)).request_floor

        if lift.weight > (0.8 * lift.capacity):
            up_requests = [request for request in sorted_picked if request.target_floor > lift.position]
            down_requests = [request for request in sorted_picked if request.target_floor < lift.position]

            if up_requests and (self.direction == Direction.UP or not down_requests):
                if self.direction != Direction.UP:
                    self.direction = Direction.UP
                return up_requests[0].target_floor
        
            if down_requests and (self.direction == Direction.DOWN or not up_requests):
                if self.direction != Direction.DOWN:
                    self.direction = Direction.DOWN
                return down_requests[-1].target_floor
        
            return None
        # Drop-offs
        for req in picked_requests:
            all_requests.append((req.target_floor, -1))

        # Pick-ups
        for req in current_requests:
            all_requests.append((req.request_floor, req.target_floor))

        # Separate and sort requests
        pick_floors = sorted([req[0] for req in all_requests if req[1] == -1 and req[0] != lift.position])
        wait_floors = sorted([(req[0], req[1]) for req in all_requests if req[1] != -1 and req[0] != lift.position], key=lambda req: req[0])

        if self.direction == Direction.UP:
            up_requests = [req[0] for req in wait_floors if req[0] > lift.position]
            if up_requests:
                return min(up_requests)  # Nearest request going up
            elif pick_floors:
                return min(pick_floors)  # Nearest drop-off going up
            else:
                self.direction = Direction.DOWN  # No requests up, switch direction

        elif self.direction == Direction.DOWN:
            down_requests = [req[0] for req in wait_floors if req[0] < lift.position]
            if down_requests:
                return max(down_requests)  # Nearest request going down
            elif pick_floors:
                return max(pick_floors)  # Nearest drop-off going down
            else:
                self.direction = Direction.UP  # No requests down, switch direction

        return None  # Stay idle if no valid moves found


class MYLIFT:
    max_batch_size = 5
    min_batch_size = 1
    scale_factor = 1
    direction = Direction.UP

    def __call__(self, lift: Lift, current_requests: list[Request], min_batch_size: int = 1, max_batch_size: int = 5, scale_factor: int = 1) -> float | None:
        if not current_requests and not lift.picked_requests:
            return None  # No requests, lift remains idle

        if lift.state == LiftState.IDLE:
            return self.find_nearest_request(lift, current_requests)

        # Prioritize requests based on weight
        if lift.weight > (0.8 * lift.capacity):
            return self.weight_handler(lift)

        # Process both picked and current requests
        return self.batching_requests(lift, current_requests, min_batch_size, max_batch_size, scale_factor)

    def find_nearest_request(self, lift, requests):
        return min(requests, key=lambda req: abs(req.request_floor - lift.position)).request_floor

    def weight_handler(self, lift):
        return self.get_next_floor(lift, lift.picked_requests, key=lambda req: req.target_floor)

    def batching_requests(self, lift, current_requests, min_batch_size, max_batch_size, scale_factor):
        all_requests = [(req.target_floor, None) for req in lift.picked_requests] + \
                       [(req.request_floor, req.target_floor) for req in current_requests]

        batch_size = max(min_batch_size, min(max_batch_size, len(all_requests) // scale_factor))
        batches = [all_requests[i:i + batch_size] for i in range(0, len(all_requests), batch_size)]

        if not batches:
            return None

        # Process each batch and find the best move
        for batch in batches:
            return self.get_travel(lift, batch)

        return None

    def get_travel(self, lift, batch):
        pick_floors = sorted(set(req[0] for req in batch if req[1] is None and req[0] != lift.position))
        wait_floors = sorted(set(req[0] for req in batch if req[1] is not None and req[0] != lift.position))

        return self.get_next_floor(lift, pick_floors + wait_floors)

    def get_next_floor(self, lift, requests, key=lambda req: req):
        if not requests:
            return None

        if self.direction == Direction.UP:
            up_requests = [req for req in requests if key(req) > lift.position]
            if up_requests:
                return min(up_requests, key=key)  # Move to nearest request going up

        if self.direction == Direction.DOWN:
            down_requests = [req for req in requests if key(req) < lift.position]
            if down_requests:
                return max(down_requests, key=key)  # Move to nearest request going down

        # If no requests match the direction, change direction
        self.direction = Direction.UP if self.direction == Direction.DOWN else Direction.DOWN
        return self.get_next_floor(lift, requests, key)  # Recurse with updated direction







        

        

        


        




        
        


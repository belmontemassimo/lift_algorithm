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
        if not current_requests and not picked_requests:
            return None # No requests, lift remains idle
        
        if lift.state == LiftState.IDLE:
            return min(current_requests, key=lambda request: abs(request.request_floor - lift.position)).request_floor
        
        all_requests = [req.target_floor for req in picked_requests] + [req.request_floor for req in current_requests]
        all_requests = sorted(set(all_requests))  # Remove duplicates and sort

        up_requests = [floor for floor in all_requests if floor > lift.position]
        down_requests = [floor for floor in all_requests if floor < lift.position]

        if up_requests and (self.direction == Direction.UP or not down_requests):
            if self.direction != Direction.UP:
                self.direction = Direction.UP
            return up_requests[0]
        
        if down_requests and (self.direction == Direction.DOWN or not up_requests):
            if self.direction != Direction.DOWN:
                self.direction = Direction.DOWN
            return down_requests[-1]
        
        return None

    
class MYLIFT:

    max_batch_size = 5
    min_batch_size = 1
    scale_factor = 1
    direction = Direction.UP
    def __call__(self, lift: Lift, current_requests: list[Request], min_batch_size: int = 1, max_batch_size: int = 5, scale_factor: int = 1) -> float | None:
        picked_requests = lift.picked_requests

        if not current_requests and not picked_requests:
            return None # No requests, lift remains idle

        if lift.state == LiftState.IDLE:
            return min(current_requests, key=lambda request: abs(request.request_floor - lift.position)).request_floor
        
        sorted_picked = sorted(picked_requests, key=lambda request: request.target_floor)
        sorted_current = sorted(current_requests, key=lambda request: request.request_floor)

        if not current_requests: #dealing with picked requests if there are no current requests in a LOOK manner
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
        
        if not picked_requests:#dealing with current requests if there are no current requests in a LOOK manner
            up_requests = [request for request in sorted_current if request.request_floor > lift.position]
            down_requests = [request for request in sorted_current if request.request_floor < lift.position]

            if up_requests and (self.direction == Direction.UP or not down_requests):
                if self.direction != Direction.UP:
                    self.direction = Direction.UP
                return up_requests[0].request_floor
            
            if down_requests and (self.direction == Direction.DOWN or not up_requests):        
                if self.direction != Direction.DOWN:
                    self.direction = Direction.DOWN
                return down_requests[-1].request_floor
            
            return None
        
        #if the weight of the lift is above 80% of the capacity, the lift will ignore current requests and only deal with picked requests
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
        
        if picked_requests and current_requests:

            all_requests = []

            # Store (floor, None) for picked requests (drop-offs)
            for req in picked_requests:
                all_requests.append((req.target_floor, None))

            # Store (request_floor, target_floor) for current requests (pick-ups)
            for req in current_requests:
                all_requests.append((req.request_floor, req.target_floor))

            # Calculate batch size dynamically
            batch_size = max(min_batch_size, min(max_batch_size, len(all_requests) // self.scale_factor))

            # Split into batches
            batches = [all_requests[i:i + batch_size] for i in range(0, len(all_requests), batch_size)]

            if not batches:
                return None  # Stay idle if no requests

            # Process each batch and find the best move
            for current_batch in batches:

                # Extract target floors (drop-offs)
                pick_floors = [req[0] for req in current_batch if req[1] is None and req[0] != lift.position]

                # Extract request floors (pick-ups)
                wait_floors = [(req[0], req[1]) for req in current_batch if req[1] is not None and req[0] != lift.position]

                # Sort drop-off requests
                pick_floors.sort()

                # Sort pick-up requests based on request floor
                wait_floors.sort(key=lambda req: req[0])

                if pick_floors or wait_floors:
                    if self.direction == Direction.UP:
                        # Get closest request going up
                        up_requests = [req[0] for req in wait_floors if req[0] > lift.position]
                        if up_requests:
                            return min(up_requests)  # Move to nearest request floor going up
                        
                        # If no pick-ups, move to nearest drop-off going up
                        if pick_floors:
                            return min(pick_floors)

                    elif self.direction == Direction.DOWN:
                        # Get closest request going down
                        down_requests = [req[0] for req in wait_floors if req[0] < lift.position]
                        if down_requests:
                            return max(down_requests)  # Move to nearest request floor going down
                        
                        # If no pick-ups, move to nearest drop-off going down
                        if pick_floors:
                            return max(pick_floors)

            return None  # Remain idle if no valid moves found


                # Serve waiting requests if they are in the direction of movement
                #if wait_floors:
                    #if self.direction == Direction.UP:
                        # Only serve current requests that are upwards
                        #up_requests = [request for request in wait_floors if request.request_floor > lift.position]
                        #if up_requests:
                            #return up_requests[0].request_floor  # Go to the next floor upwards
                    #elif self.direction == Direction.DOWN:
                        # Only serve current requests that are downwards
                        #down_requests = [request for request in wait_floors if request.request_floor < lift.position]
                        #if down_requests:
                            #return down_requests[-1].request_floor  # Go to the next floor downwards




        

        

        


        




        
        


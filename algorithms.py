from request import Request
from lift import Lift
from lift import LiftState
from inspect import getmembers, isclass
from importlib import import_module

def get_algorithms() -> dict[str,object]:
    module = import_module("algorithms")
    return {algorithm_name: algorithm_class for algorithm_name, algorithm_class in getmembers(module, isclass) if algorithm_class.__module__ == module.__name__ and algorithm_name != "AlgorithmHandler"}

class AlgorithmHandler:
    algorithm: object
    algorithms: dict[str,object]

    def __init__(self):
        self.algorithm = FCFS()
        self.algorithms = get_algorithms()

    def __call__(self, lift: Lift, current_requests: list[Request], picked_requests: list[Request]):
        return self.algorithm(lift, current_requests, picked_requests)

    def get_list(self) -> dict[str,object]:
        return list(self.algorithms.keys())
    
    def set_algorithm(self, algorithm_name: str):
        self.algorithm = self.algorithms[algorithm_name]()

# create algorithm class for each algorithm
class FCFS:
    def __call__(self, lift: Lift, current_requests: list[Request], picked_requests: list[Request]) -> float:
        if picked_requests:
            return picked_requests[0].target_floor
        
        if current_requests:
            return current_requests[0].request_floor
        
        return None


class SCAN:
    def __call__(self, lift: Lift, current_requests: list[Request], picked_requests: list[Request]) -> None:
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


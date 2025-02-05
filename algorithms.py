from request import Request
from lift import Lift


# create algorithm class for each algorithm
class FCFS:
    def run(self, lift: Lift, current_requests: list[Request], picked_requests: list[Request]) -> float:
        if picked_requests:
            return picked_requests[0].target_floor
        
        if current_requests:
            return current_requests[0].request_floor
        
        return None


class SCAN:
    def run(self, lift: Lift, current_requests: list[Request], picked_requests: list[Request]) -> float:
        if not current_requests and not picked_requests:
            return None  # No requests, stay on the same floor

        # Get all floors from requests
        all_requests = [req.target_floor for req in picked_requests] + [req.request_floor for req in current_requests]
        all_requests = sorted(set(all_requests))  # Remove duplicates and sort

        # Move in the current direction
        if Request.direction == 1:
            # Get next highest floor
            for floor in all_requests:
                if floor >= lift.current_floor:
                    return floor
            # If no more requests above, change direction
            Request.direction = -1
            return max(all_requests)  # Move to the highest request before reversing
        
        elif Request.direction == -1:
            # Get next lowest floor
            for floor in reversed(all_requests):
                if floor <= lift.current_floor:
                    return floor
            # If no more requests below, change direction
            Request.direction = 1
            return min(all_requests)  # Move to the lowest request before reversing

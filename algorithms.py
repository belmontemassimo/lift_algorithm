from request import Request
from lift import Lift


# create algorithm class for each algorithm
class fcfs:

    def run(self,lift: Lift , current_requests: list[Request], picked_requests: list[Request]) -> float:
        for picked_request in picked_requests:
            return picked_request.target_floor
        for request in current_requests:
            return request.request_floor
        return None
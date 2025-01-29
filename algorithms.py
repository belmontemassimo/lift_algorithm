from request import Request
from lift import Lift

class fcfs:

    def run(self,lift: Lift , list_of_requests: list[Request], picked_requests: list[Request]) -> Request:
        for picked_request in picked_requests:
            return picked_request
        for request in list_of_requests:
            return request
        return None
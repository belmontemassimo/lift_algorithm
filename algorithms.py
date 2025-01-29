from request import Request

class fcfs:

    def run(self, list_of_requests: list[Request], picked_requests: list[Request]) -> Request:
        for picked_request in picked_requests:
            return picked_request
        for request in list_of_requests:
            return request
        return None
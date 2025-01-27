import heapq
import time

class Request:
    def __init__(self, target_floor: int, time_created: float, direction:str):
        self.target_floor = target_floor
        self.time_created = time_created
        self.direction = direction


    def waiting_time(self):
        return time.time()- self.time_created

    # compares the waited times
    def __lt__(self, other_request: float):
        # if other is not a Request object, return NotImplemented
        if not isinstance(other_request, Request):
            return NotImplemented
        return self.waiting_time() < other_request.waiting_time()


# testing code

# Create a priority queue (min-heap)
if __name__ == "__main__":
    heap = []

    # Add requests to the heap
    heapq.heappush(heap, Request(target_floor=5, time_created=time.time() - 10, direction="up"))
    heapq.heappush(heap, Request(target_floor=2, time_created=time.time() - 5, direction="down"))

    # Process requests
    while heap:
        next_request = heapq.heappop(heap)
        print(f"Processing request to floor {next_request.target_floor}, waited {next_request.waiting_time():.2f} seconds")

    

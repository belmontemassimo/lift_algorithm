from extenders import double_normal_distribution
from extenders import Direction

# class that represcent entire request from start to finish
class Request:
    # variables definition
    request_floor: int
    target_floor: int
    time_created: float    
    time_on_floor: float
    time_in_lift: float
    weight_captor: int
    direction: Direction
    lift_position_on_request: float | None  # Position of the lift when request was received
    assigned_lift_id: int | None  # ID of the lift that eventually handled the request

    # init request 
    def __init__(self, request_floor:int , target_floor: int, time_created: float, weight_captor: int = 0):
        self.request_floor = request_floor
        self.target_floor = target_floor
        self.time_created = time_created
        # determine direction of request (button press simulation)
        self.direction = Direction.UP if (request_floor-target_floor) < 0 else Direction.DOWN
        self.lift_position_on_request = None  # Initialize as None
        self.assigned_lift_id = None  # Initialize as None
        # set weight to custom if provided
        if weight_captor != 0:
            self.weight_captor = weight_captor
        # generate random weight under a normal distribution
        else:
            self.weight_captor = int(double_normal_distribution(mean=70, std_dev=12.5, second_mean=3.5, second_std_dev=0.5)*100)


    def waiting_time(self, current_time: float) -> float:
        return current_time - self.time_created
    
    # saves time from request appearing to lift arrival
    def lift_check_in(self, time: float):
        self.time_on_floor = time - self.time_created
        return True
    
    # saves time from lift arrival to request completion
    def floor_check_in(self, time: float):
        self.time_in_lift = time - self.time_on_floor
        return True
    
    # creates a list of all floor numbers between two specified floors based on the direction of the lift
    def floors_range(self, start_floor:float, end_floor:int) -> list[int]:
        if start_floor > end_floor:
            start_floor = start_floor.__floor__()
            
        else:
            start_floor = start_floor.__ceil__()

        return list(range(min(start_floor,end_floor),max(start_floor,end_floor)+1))

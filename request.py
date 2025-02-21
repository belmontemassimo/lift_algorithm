from enum import Enum
from extenders import double_normal_distribution
from lift import Lift, LiftState
 
class Direction(Enum):
    UP = 1
    DOWN = -1

class Request:
    request_floor: int
    target_floor: int
    time_created: float    
    time_on_floor: float
    time_in_lift: float
    weight_captor: int
    direction: Direction

    def __init__(self, request_floor:int , target_floor: int, time_created: float, weight_captor: int = 0):
        self.request_floor = request_floor
        self.target_floor = target_floor
        self.time_created = time_created
        self.direction = Direction.UP if (request_floor-target_floor) < 0 else Direction.DOWN
        if weight_captor != 0:
            self.weight_captor = weight_captor * 100
        else:
            self.weight_captor = int(double_normal_distribution(mean=70, std_dev=12.5, second_mean=3.5, second_std_dev=0.5)*100)


    def waiting_time(self, current_time: float) -> float:
        return current_time - self.time_created
    
    def lift_check_in(self, time: float):
        self.time_on_floor = time - self.time_created
        return True
    
    def floor_check_in(self, time: float):
        self.time_in_lift = time - self.time_on_floor
        return True

    def get_floors_between_requests(self, current_position: float, target_position: float) -> list[int]:
        """
        Returns a list of floors that will be passed between current_position and target_position.
        The list includes both start and end floors.
        
        Args:
            current_position (float): Current position of the lift
            target_position (float): Target position the lift is moving to
            
        Returns:
            list[int]: List of floors that will be passed, in order of passing
        """
        # Round positions to handle floating point positions
        start_floor = round(current_position)
        end_floor = round(target_position)
        
        # Determine direction of movement
        step = 1 if start_floor < end_floor else -1
        
        # Generate list of floors including start and end
        return list(range(start_floor, end_floor + step, step))

    def get_closest_lift(self, lifts: list['Lift']) -> Lift | None:
        """
        Returns the closest idle lift to handle this request.
        
        Args:
            lifts (list[Lift]): List of all available lifts
            
        Returns:
            Lift: The closest idle lift to the request floor
        """
        idle_lifts = [lift for lift in lifts if lift.state == LiftState.IDLE]
        if not idle_lifts:
            return None
        
        return min(idle_lifts, key=lambda lift: abs(lift.position - self.request_floor))

    
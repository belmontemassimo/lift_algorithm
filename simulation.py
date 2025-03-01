#
# this is a main file that must be used to run any code
#

from gui import run_gui, gui_update
from lift import LiftState
from extenders import DeltaTime, set_time_multiplier
from generator import load_sample
from request import Request
from algorithms import AlgorithmHandler
from monitoring import run_monitoring, update_monitoring
from liftmanager import LiftManager
from graph import SimulationAnalytics

# function to run entier simulation
def run_simulation(isGUI: bool = True):
    # set lift configuration constants
    MAX_SPEED: float = 2
    ACCELERATION: float = 1
    CAPACITY: float = 1500
    WAITING_TIME: float = 10

    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = []
    # save initial number of requests
    len_list_of_requests: int = len(list_of_requests)
    floors = 0
    # two lists to keep track of active and completed requests
    current_requests: list[Request] = []
    completed_requests_list: list[Request] = []
    # class that contains algorithms¥
    algorithm = AlgorithmHandler()
    
    # init lift managet and analytics
    lift_manager = LiftManager()
    analytics = SimulationAnalytics()
    
    # Then create monitoring with the lift_manager
    monitoring_queue = run_monitoring(algorithm.get_list(), CAPACITY)
    
    # Initialize gui_queue to None
    gui_queue = None

    # flag to show if any changes in simulation (new request, lift stoped, etc)
    update_flag: bool = True
    
    # Wait for start signal from monitoring and configure lift manager after 
    while True:
        if not monitoring_queue.empty():
            data = monitoring_queue.get()
            if data["sample"]:
                list_of_requests = load_sample(data["sample"])
                len_list_of_requests = len(list_of_requests)
            for request in list_of_requests:
                if max(request.target_floor, request.request_floor) > floors:
                    floors = max(request.target_floor, request.request_floor)
            floors += 1
            lift_manager.configure(floors, data["lifts"], MAX_SPEED, ACCELERATION, CAPACITY, WAITING_TIME)
            set_time_multiplier(data["time"])
            algorithm.set_algorithm(data["algorithm"])
            if isGUI:
                gui_queue = run_gui(floors, data["lifts"])
            break
        
    
    # init items to keep tracj if time
    timer = 0
    deltatime = DeltaTime()
    RECORD_INTERVAL = 0.1  # Record every 0.1 seconds
    next_record_time = 0
    
    while True: 
        # timer update
        timer += deltatime()
        # update lifts
        lift_manager.run_updates()
        
        # records lifts statictics with set interval 
        if timer >= next_record_time:
            analytics.record_state(timer, lift_manager.lifts)
            next_record_time += RECORD_INTERVAL

        # update of monitoring and gui if enabled
        update_monitoring(monitoring_queue, lift_manager, timer)
        if isGUI and gui_queue is not None:
            gui_update(lift_manager, gui_queue)

        # collects requestes that become due after the last loop
        new_requests_list = [request for request in list_of_requests if timer >= request.time_created]
        # if there is a request in new_requests_list then add it to the current_requests list 
        if new_requests_list:
            # Record the lift positions for each new request
            for request in new_requests_list:
                # Record position of all lifts at the time of request
                lift_positions = lift_manager.get_positions()
                # Find the closest lift 
                closest_lift_idx = min(range(len(lift_positions)), 
                                      key=lambda i: abs(lift_positions[i] - request.request_floor))
                # Store the position of the closest lift for graph analytics
                request.lift_position_on_request = lift_positions[closest_lift_idx]
                    
            current_requests.extend(new_requests_list)
            # removes the processed request from the list_of_requests
            list_of_requests = [request for request in list_of_requests if request not in new_requests_list]
            update_flag = True
        
        # for loop to determin if requests are required to interact with LiftState 
        for lift_idx, lift in enumerate(lift_manager.lifts):
            match lift.state:
                case LiftState.WAITING:
                    # adds all requests from the floor where lift is at 
                    add_requests_list: list[Request] = [request for request in current_requests if request.request_floor == lift.position and lift.add_request(request) and request.lift_check_in(timer)]
                    # update list of waiting requests if there are new requests moved to the lift
                    if add_requests_list:
                        # Record the actual lift that handled each request (no longer needed for graphs)
                        current_requests = [request for request in current_requests if request not in add_requests_list]
                        update_flag = True
                    # check if request reached the target floor and process accordingly 
                    if (lambda new_items: completed_requests_list.extend(new_items) or new_items)([request for request in lift.picked_requests if request.target_floor == lift.position and request.floor_check_in(timer) and lift.remove_request(request)]):
                        update_flag = True
                case LiftState.AFTERWAIT:
                    # call algorithm update if lift is ready to depart
                    update_flag = True

        # check if update is needed
        if update_flag:
            update_flag = False
            next_floors = algorithm(lift_manager, current_requests)
            # set target floors from algorithm output
            lift_manager.set_target_floors([floor if floor != None else 0 for floor in next_floors])
            states = lift_manager.get_states()
            # set lifts states accordingly to the new target floor and previous state
            lift_manager.set_states([(LiftState.IDLE if states[i] != LiftState.WAITING else states[i]) if floor == None else (LiftState.MOVING if states[i] == LiftState.IDLE or states[i] == LiftState.AFTERWAIT else states[i]) for i, floor in enumerate(next_floors)])

            # stop simulation loop if number if delivered requests is equal to initial number of requests 
            if len_list_of_requests == len(completed_requests_list):
                break
                
    # generate analytics after simulation is finished
    analytics.generate_graphs(completed_requests_list, timer)
    return analytics

# main function
if __name__ == "__main__":
    run_simulation()

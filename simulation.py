#
# this is a main file that must be used to run any code
#

from multiprocessing import Queue
from gui import run_gui, gui_update
from lift import LiftState
from extenders import DeltaTime, set_time_multiplier
from request import Request
from algorithms import AlgorithmHandler
from monitoring import run_monitoring, update_monitoring
from liftmanager import LiftManager
from graph import SimulationAnalytics


def run_simulation(isGUI: bool = True):
    max_speed: float = 2
    acceleration: float = 0.4
    capacity: float = 1000
    waiting_time: float = 4

    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = [Request(5,0,0), Request(8, 2, 3), Request(2, 1, 20), Request(3, 20, 21), Request(4, 1, 24), Request(5, 1, 25), 
                                    Request(6, 1, 26), Request(7, 1, 27), Request(8, 1, 28), Request(9, 1, 29), Request(10, 1, 30), Request(11, 1, 31), 
                                    Request(12, 1, 32), Request(13, 1, 33), Request(14, 1, 34), Request(15, 1, 35), Request(16, 1, 36), Request(17, 1, 37), 
                                    Request(18, 1, 38), Request(19, 1, 39), Request(20, 1, 40), Request(21, 1, 41), Request(22, 1, 42), Request(23, 1, 43)]
    len_list_of_requests: int = len(list_of_requests)
    current_requests: list[Request] = []
    completed_requests_list: list[Request] = []
    algorithm = AlgorithmHandler()
    
    # Create lift manager first
    lift_manager = LiftManager()
    analytics = SimulationAnalytics()
    
    # Then create monitoring with the lift_manager
    monitoring_queue = run_monitoring(algorithm.get_list(), capacity)

    # TEMP
    update_flag: bool = False
    
    # Wait for start signal from monitoring
    while True:
        if not monitoring_queue.empty():
            data = monitoring_queue.get()
            lift_manager.configure(data["floors"], data["lifts"], max_speed, acceleration, capacity, waiting_time)
            set_time_multiplier(data["time"])
            algorithm.set_algorithm(data["algorithm"])
            if isGUI:
                gui_queue = run_gui(data["floors"], data["lifts"])
            break
        
    
    # set a timer so that we can see the efficiency of the algorithm based on a set of requests
    timer = 0
    deltatime = DeltaTime()
    
    while True: 
        timer += deltatime()
        # update lifts
        lift_manager.run_updates()

        # record the state of the lifts
        #analytics.record_state(timer, lift_manager.lifts)

        # allow the user to disable the monitoring and the gui
        update_monitoring(monitoring_queue, lift_manager, timer)
        if isGUI:
            gui_update(lift_manager, gui_queue)

        new_requests_list = [request for request in list_of_requests if timer >= request.time_created]
        # if there is a request in new_requests_list then add it to the current_requests list 
        if new_requests_list:
            current_requests.extend(new_requests_list)
            # removes the processed request from the list_of_requests
            list_of_requests = [request for request in list_of_requests if request not in new_requests_list]
            update_flag = True

        for lift in lift_manager.lifts:
            match lift.state:
                case LiftState.WAITING:
                    # checks for every lift if it is at the floor where someone called it
                    add_requests_list: list[Request] = [request for request in current_requests if request.request_floor == lift.position and lift.add_request(request) and request.lift_check_in(timer)]
                    if add_requests_list:
                        current_requests = [request for request in current_requests if request not in add_requests_list]
                        update_flag = True
                    # checks if someone arrived at it's target floor 
                    if (lambda new_items: completed_requests_list.extend(new_items) or new_items)([request for request in lift.picked_requests if request.target_floor == lift.position and request.floor_check_in(timer) and lift.remove_request(request)]):
                        update_flag = True
                case LiftState.AFTERWAIT:
                    update_flag = True

        if update_flag:
            update_flag = False
            next_floors = algorithm(lift_manager, current_requests)
            lift_manager.set_target_floors([floor if floor != None else 0 for floor in next_floors])
            states = lift_manager.get_states()
            lift_manager.set_states([(LiftState.IDLE if states[i] != LiftState.WAITING else states[i]) if floor == None else (LiftState.MOVING if states[i] == LiftState.IDLE or states[i] == LiftState.AFTERWAIT else states[i]) for i, floor in enumerate(next_floors)])

            if len_list_of_requests == len(completed_requests_list):
                break
                
    analytics.generate_graphs(completed_requests_list, timer)
    return analytics

if __name__ == "__main__":
    run_simulation()

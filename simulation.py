#
# this is a main file that must be used to run any code
#

from gui import run_gui, gui_update
from lift import LiftState
from extenders import DeltaTime, set_time_multiplier
from request import Request
from algorithms import AlgorithmHandler
from monitoring import Monitoring
from liftmanager import LiftManager

if __name__ == "__main__":

    isMonitoring: bool = True
    isGUI: bool = True
    num_floors: int = 30
    num_lifts: int = 3 # PLEASE DO NOT SET MORE THEN 3, NOT ALL MODULES ARE READY FOR IT :)
    max_speed: float = 2
    acceleration: float = 0.4
    capacity: float = 1000
    waiting_time: float = 4

    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = [Request(5,0,0), Request(8, 2, 3), Request(2, 1, 20), Request(3, 20, 21), Request(4, 1, 24), Request(5, 1, 25), 
                                       Request(6, 1, 26), Request(7, 1, 27), Request(8, 1, 28), Request(9, 1, 29), Request(10, 1, 30), Request(11, 1, 31), 
                                       Request(12, 1, 32), Request(13, 1, 33), Request(14, 1, 34), Request(15, 1, 35), Request(16, 1, 36), Request(17, 1, 37), 
                                       Request(18, 1, 38), Request(19, 1, 39), Request(20, 1, 40), Request(21, 1, 41), Request(22, 1, 42), Request(23, 1, 43)]
    current_requests: list[Request] = []
    algorithm = AlgorithmHandler()
    

    # temporary solution for testing purposes
    lift_manager = LiftManager(num_floors, num_lifts, max_speed, acceleration, capacity, waiting_time)
    if isMonitoring:
        monitoring = Monitoring(lift_manager, algorithm)
    else:
        algorithm.set_algorithm("FCFS")
        set_time_multiplier(1)
    if isGUI:
        gui_possition_queue = run_gui(num_floors, num_lifts)

    # output lifts positions constantly

    timer = 0
    deltatime = DeltaTime()
    while True: 
        timer += deltatime()
        lift_manager.run_updates()
        if isMonitoring:
            monitoring.update(timer)
        if isGUI:
            gui_update(lift_manager, gui_possition_queue)

        new_requests_list = [request for request in list_of_requests if timer >= request.time_created]
        if new_requests_list:
            current_requests.extend(new_requests_list)
            list_of_requests = [request for request in list_of_requests if request not in new_requests_list]

       
        for lift in lift_manager.lifts:
            if lift.state == LiftState.WAITING:
                 # checks for every lift if it is at the floor where someone called it
                add_requests_list: list[Request] = [request for request in current_requests if request.request_floor == lift.position and lift.add_request(request)]
                if add_requests_list:
                    current_requests = [request for request in current_requests if request not in add_requests_list]
                # checks if someone arrived at it's target floor (the floor he wanted to go to)
                # this variable is temporary not in use but is very important
                remove_requests_list: list[Request] = [request for request in lift.picked_requests if request.target_floor == lift.position and lift.remove_request(request)]

            next_floor = algorithm(lift, current_requests)
            # put lift into idle if there is no requests 
            if next_floor == None:
                lift.target_floor = 0
                if lift.state != LiftState.WAITING:
                    lift.state = LiftState.IDLE
                # set lift on motion to the next floor
            else:
                lift.target_floor = next_floor
                if lift.state == LiftState.IDLE or lift.state == LiftState.AFTERWAIT:
                    lift.state = LiftState.MOVING


        
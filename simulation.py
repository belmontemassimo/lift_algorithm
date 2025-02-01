#
# this is a main file that must be used to run any code
#

from gui import run_gui, gui_update
from time import sleep
from lift import LiftState, Lift
from extenders import DeltaTime, set_time_multiplier
from request import Request
from algorithms import fcfs
from monitoring import Monitoring
from liftmanager import LiftManager

if __name__ == "__main__":

    # place for all config variables (please nothing above this comment)
    set_time_multiplier(5)

    num_floors = 30
    num_lifts = 1

    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = [Request(5,0,0), Request(8, 2, 3), Request(2, 1, 20), Request(3, 20, 29), Request(4, 1, 180)]
    current_requests: list[Request] = []
    algorithm = fcfs()
    

    # temporary solution for testing purposes
    lift_manager = LiftManager(num_floors, num_lifts, 2, 0.4, 1000, 4)
    monitoring = Monitoring(lift_manager)
    gui_possition_queue = run_gui(num_floors, num_lifts)

    # output lifts positions constantly

    timer = 0
    deltatime = DeltaTime()
    while True: 
        timer += deltatime()
        lift_manager.run_updates()
        monitoring.update(timer)
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

        # TEMPORARY PART TO ACCOMODATWE ONLY ONE LIFT
        if lift_manager.num_lifts == 1:
            lift: Lift = lift_manager.lifts[0]
            next_floor= algorithm.run(lift, current_requests, lift.picked_requests)
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


        
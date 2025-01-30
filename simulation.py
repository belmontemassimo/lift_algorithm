#
# this is a main file that must be used to run any code
#

from gui import GUI
from time import sleep
from lift import LiftState, Lift
from extenders import DeltaTime, set_time_multiplier
from request import Request
from algorithms import fcfs
from liftmanager import LiftManager

if __name__ == "__main__":

    # place for all config variables (please nothing above this comment)
    set_time_multiplier(1)

    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = [Request(5,0,0), Request(8, 2, 3), Request(2, 1, 20), Request(3, 20, 29), Request(4, 1, 180)]
    current_requests: list[Request] = []
    algorithm = fcfs()
    

    # temporary solution for testing purposes
    lift_manager = LiftManager(20, 1, 2, 0.4, 1000, 4)

    # output lifts positions constantly

    timer = 0
    deltatime = DeltaTime()
    while True: 
        timer += deltatime()
        lift_manager.run_updates()

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
        if len(lift_manager.lifts) == 1:
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
 
        print("")
        print(f"time: {"%.2f" % timer}")
        print(f'position:      {"%.2f" % lift_manager.get_positions()[0]}')
        print(f'speed:         {"%.2f" % lift_manager.get_speed()[0]}')
        state = lift_manager.get_states()[0]
        print(f'state:         {"waiting" if state == LiftState.WAITING else "idle" if state == LiftState.IDLE else "moving"}')
        print(f'weight:        {lift_manager.get_weight()[0]}/{lift_manager.capacity}')
        print("target floors: ", end="")
        print(*lift_manager.get_target_floors())
        sleep(0.01)


        
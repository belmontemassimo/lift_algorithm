#
# this is a main file that must be used to run any code
#

import gui
import time
from lift import LiftState, Lift
from extenders import DeltaTime, set_time_multiplier
from request import Request
from algorithms import fcfs
import liftmanager

if __name__ == "__main__":
    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = [Request(5,0,0), Request(8, 2, 3), Request(2, 1, 20), Request(3, 20, 29), Request(4, 1, 180)]
    current_requests: list[Request] = []
    algorithm = fcfs()
    set_time_multiplier(1)

    # temporary solution for testing purposes
    lift_manager = liftmanager.LiftManager(10, 1, 2, 0.4, 1000, 4)

    # output lifts positions constantly

    timer = 0
    deltatime_obj = DeltaTime()
    while True: 
        deltatime = deltatime_obj()
        timer += deltatime
        lift_manager.run_updates()
        poss = lift_manager.get_positions()
        speed = lift_manager.get_speed()
        states = lift_manager.get_states()
        
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
                remove_requests_list: list[Request] = [request for request in lift.picked_requests if request.target_floor == lift.position]
                if remove_requests_list:
                    lift.picked_requests = [request for request in lift.picked_requests if request not in remove_requests_list]

        # TEMPORARY PART TO ACCOMODATWE ONLY ONE LIFT
        if len(lift_manager.lifts) == 1:
            lift: Lift = lift_manager.lifts[0]
            next_floor= algorithm.run(lift, current_requests, lift.picked_requests)
            if next_floor == None:
                lift.target_floor = 0
                if lift.state != LiftState.WAITING:
                    lift.state = LiftState.IDLE
            else:
                lift.target_floor = next_floor
                if lift.state == LiftState.IDLE or lift.state == LiftState.AFTERWAIT:
                    lift.state = LiftState.MOVING
 
        print("")
        print(f"time: {"%.2f" % timer}")
        print(f'position:      {"%.2f" % poss[0]}')
        print(f'speed:         {"%.2f" % speed[0]}')
        print(f'state:         {"waiting" if states[0] == LiftState.WAITING else "idle" if states[0] == LiftState.IDLE else "moving"}')
        print("target floors: ", end="")
        print(*lift_manager.get_target_floors(), sep="   ")
        time.sleep(0.01)


        
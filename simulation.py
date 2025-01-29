#
# this is a main file that must be used to run any code
#

import gui
import time
from lift import LiftState
from extenders import DeltaTime, set_time_multiplier
from algorithms import Request
import liftmanager

if __name__ == "__main__":
    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests: list[Request] = [Request(5,0,0), Request(8, 2, 3), Request(2, 1, 20), Request(3, 0, 29), Request(4, 1, 57)]
    current_requests = []
    set_time_multiplier(2)

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
        if list_of_requests and timer >= list_of_requests[0].time_created:
            current_requests.append(list_of_requests.pop(0))

        print(f'position:      {"%.2f" % poss[0]}')
        print(f'speed:         {"%.2f" % speed[0]}')
        print(f'state:         {states[0]}')
        print("target floors: ", end="")
        print(*lift_manager.get_target_floors(), sep="   ")
        time.sleep(0.05)


        
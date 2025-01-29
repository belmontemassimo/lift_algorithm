#
# this is a main file that must be used to run any code
#

import gui
import time
from lift import LiftState
import extenders
import liftmanager

if __name__ == "__main__":
    # requests are in the form of (target_floor, direction, time_created)
    list_of_requests = [(5, 0, 0), (8, 2, 3), (2, 1, 20), (3, 0, 29), (4, 1, 57)]
    current_requests = []
    extenders.set_time_multiplier(2)

    # temporary solution for testing purposes
    lift_manager = liftmanager.LiftManager(10, 3, 2, 0.4, 1000, 4)
    lift_manager.set_target_floors([9])
    lift_manager.set_lifts_states([LiftState.MOVING])

    # output lifts positions constantly

    timer = 0
    deltatime = extenders.DeltaTime()
    while True: 
        lift_manager.run_updates()
        poss = lift_manager.lifts_positions()
        speed = lift_manager.lifts_speed()
        states = lift_manager.get_lifts_states()
        deltatime = deltatime()
        timer += deltatime
        if list_of_requests and timer >= list_of_requests[0][2]:

            current_requests.append(list_of_requests.pop(0))

        print(f'position:      {"%.2f" % poss[0]}')
        print(f'speed:         {"%.2f" % speed[0]}')
        print(f'state:         {states[0]}')
        print("target floors: ", end="")
        print(*lift_manager.get_target_floors(), sep="   ")
        time.sleep(0.05)


        
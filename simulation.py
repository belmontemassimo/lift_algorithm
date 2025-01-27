#
# this is a main file that must be used to run any code
#

import gui
import time
from lift import LiftState
import liftmanager

if __name__ == "__main__":

    # temporary solution for testing purposes
    lift_manager = liftmanager.LiftManager(10, 3, 2, 0.4, 10, 4)
    lift_manager.set_target_floors([10, 15, 5])
    lift_manager.set_lifts_states([LiftState.MOVING, LiftState.MOVING, LiftState.MOVING])

    # output lifts positions constantly
    while True:
        poss = lift_manager.lifts_positions()
        speed = lift_manager.lifts_speed()
        states = lift_manager.get_lifts_states()
        print(f'position:      {"%.2f" % poss[0]} {"%.2f" % poss[1]} {"%.2f" % poss[2]}')
        print(f'speed:         {"%.2f" % speed[0]} {"%.2f" % speed[1]} {"%.2f" % speed[2]}')
        print(f'state:         {states[0]} {states[1]} {states[2]}')
        print("target floors: ", end="")
        print(*lift_manager.get_target_floors(), sep="   ")

        if lift_manager.get_lifts_states()[1] == LiftState.AFTERWAIT:
            lift_manager.set_target_floors([10, 5, 5])
            lift_manager.set_lifts_states([LiftState.IDLE, LiftState.MOVING, LiftState.IDLE])

        time.sleep(0.05)


        
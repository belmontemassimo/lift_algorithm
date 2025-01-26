#
# this is a main file that must be used to run any code
#

import gui
import time
import liftmanager

if __name__ == "__main__":

    # temporary solution for testing purposes
    lift_manager = liftmanager.LiftManager(10, 3, 2, 0.5, 10)
    lift_manager.target_floors[0][0] = 10
    lift_manager.target_floors[1][0] = 15
    lift_manager.target_floors[2][0] = 8

    # output lifts positions constantly
    while True:
        poss = lift_manager.lifts_positions()
        print(f'{"%.2f" % poss[0]} {"%.2f" % poss[1]} {"%.2f" % poss[2]}')
        time.sleep(0.1)


        
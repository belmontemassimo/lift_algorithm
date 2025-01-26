#
# this is a main file that must be used to run any code
#

import gui
import time
import liftmanager

if __name__ == "__main__":

    # temporary solution for testing purposes
    lift_manager = liftmanager.LiftManager(10, 3, 2, 0.5, 10)
    lift_manager.set_target_floors([5, 7, 2])

    # output lifts positions constantly
    while True:
        poss = lift_manager.lifts_positions()
        print(f'{"%.2f" % poss[0]} {"%.2f" % poss[1]} {"%.2f" % poss[2]}')
        print(f'{lift_manager.get_target_floors()}')
        time.sleep(0.05)


        
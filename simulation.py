import gui
import lift
import time
import os
import liftmanager

if __name__ == "__main__":

    lift_manager = liftmanager.LiftManager(10, 3, 2, 0.5, 10)
    lift_manager.target_floors[0][0] = 10
    lift_manager.target_floors[1][0] = 15
    lift_manager.target_floors[2][0] = 8
    while True:
        poss = lift_manager.lifts_positions()
        print(f'{"%.2f" % poss[0]} {"%.2f" % poss[1]} {"%.2f" % poss[2]}')
        time.sleep(0.1)


        
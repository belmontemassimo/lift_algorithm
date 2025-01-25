import gui
import lift
import time
import os

if __name__ == "__main__":
    
    prev_message_length = 0


    lift = lift.Lift(capacity=5, max_speed=1, acceleration=0.2)
    lift.move_to(8)
    while True:
        lift.update()
        print("\033c") 
        print(f"speed: {lift.speed}")
        print(f"position: {lift.position}")
        print(f"target_floor: {lift.target_floor}")
        time.sleep(0.001)


        
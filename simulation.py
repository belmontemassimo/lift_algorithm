import gui
import lift
import extenders
import time

if __name__ == "__main__":
    
    lift = lift.Lift(capacity=5, max_speed=1, acceleration=0.2)
    lift.move_to(4)
    while True:
        lift.update()
        print(lift.position)
        print(f"speed: {lift.speed}")
        time.sleep(0.1)
        
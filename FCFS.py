import tkinter as tk
import time

class Ascenseur:
    '''
    handles the graphical representation of the lift
    '''
    def __init__(self, canvas, total_floors):
        self.canvas = canvas
        self.current_floor = 0 # current floor
        self.floors = list(range(total_floors)) # list of floors
        self.speed = 1
        self.status = 0
        self.floor_coords = [] # y value of different floors
        canvas.update()

        n_stops = canvas.winfo_height() / total_floors 
        height = canvas.winfo_height()

        for i in range(total_floors):
            bottom_coord = height - (i * n_stops)
            self.floor_coords.append(bottom_coord)
            canvas.create_line(0, bottom_coord, canvas.winfo_width(), bottom_coord, fill="black", width=2)
            canvas.create_text(10, bottom_coord - (n_stops / 2), text=str(i), fill="black", font=("Arial", 12, "bold"))
        
        self.id = canvas.create_rectangle(
            40,
            self.floor_coords[0],
            40 + n_stops,
            self.floor_coords[0] - n_stops,
            fill='black'
        )

    def move_down(self, target_floor, callback):
        '''
        moves the lift down to the target floor
        calls callback when the lift has reached the target floor
        '''
        self.status = 1
        bottom_coords = self.canvas.coords(self.id)[3]
        target_coords = self.floor_coords[target_floor]
        
        if bottom_coords < target_coords:
            self.canvas.move(self.id, 0, self.speed)
            self.canvas.after(10, lambda: self.move_down(target_floor, callback))
        else:
            time.sleep(1)
            self.status = 0
            callback()

    def move_up(self, target_floor, callback):
        '''
        moves the lift up to the target floor
        '''
        self.status = 1
        bottom_coords = self.canvas.coords(self.id)[3]
        target_coords = self.floor_coords[target_floor]
        
        if bottom_coords > target_coords:
            self.canvas.move(self.id, 0, -self.speed)
            self.canvas.after(10, lambda: self.move_up(target_floor, callback))
        else:
            time.sleep(1)
            self.status = 0
            callback()

    def move_to_floor(self, target_floor, callback):
        '''
        decides whether to move up or down based on the target floor
        '''
        if target_floor > self.current_floor:
            self.move_up(target_floor, callback)
        elif target_floor < self.current_floor:
            self.move_down(target_floor, callback)
        else:
            callback()

    def update_floor(self):
        '''
        checks the lifts position on the canvas
        updates the current floor if the lift has moved
        prints the current floor to the console
        '''
        bottom_coords = self.canvas.coords(self.id)[3]
        for i, coord in enumerate(self.floor_coords):
            if i < len(self.floor_coords) - 1 and bottom_coords <= coord and bottom_coords > self.floor_coords[i + 1]:
                if self.current_floor != i:
                    self.current_floor = i
                    print(f"Lift position: {self.current_floor}")
        self.canvas.after(10, self.update_floor)


class LiftSystem:
    '''
    manages the requests for the lift for a first come first serve basis
    takes an instance of the Ascenseur class as an argument
    '''
    def __init__(self, ascenseur_instance):
        self.lift = ascenseur_instance# Ascenseur(canvas, floors)
        self.requests = []# list of floors requested
        self.processing = False# flag to check if the lift is processing a request

    def request_floor(self, floor):
        # adds the requested floor to the list of requests
        if floor not in self.requests:
            self.requests.append(floor)
            print(f"Floor {floor} requested.")
        self.process_requests()# process the requests

    def process_requests(self):
        # if the lift is not processing a request and there are requests in the list
        if not self.processing and self.requests:
            self.processing = True
            next_floor = self.requests.pop(0)
            print(f"Processing request for floor {next_floor}.")
            self.lift.move_to_floor(next_floor, self.request_complete)

    def request_complete(self):
        # prints the current floor when the lift has reached the target floor
        print(f"Arrived at floor {self.lift.current_floor}.")
        self.processing = False
        self.process_requests()


if __name__ == "__main__":
    import threading

    root = tk.Tk()
    root.title("Lift Simulation")
    canvas = tk.Canvas(root, width=800, height=1000, bg='white')
    canvas.pack()

    floors = 10
    ascenseur_instance = Ascenseur(canvas, floors)
    lift_system = LiftSystem(ascenseur_instance)

    ascenseur_instance.update_floor()

    def request_floors_dynamically():
        ''' Continuously prompt the user for floor requests in a separate thread '''
        while True:
            try:
                # Get user input for the next floor
                floor = int(input("Enter a floor to request (or -1 to quit): "))
                if floor == -1:  # Exit condition
                    print("Exiting floor request input.")
                    break
                elif 0 <= floor < floors:
                    lift_system.request_floor(floor)
                else:
                    print(f"Invalid floor. Please enter a number between 0 and {floors - 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid floor number.")

    # Run the input loop in a separate thread to avoid blocking the GUI
    threading.Thread(target=request_floors_dynamically, daemon=True).start()

    root.mainloop()


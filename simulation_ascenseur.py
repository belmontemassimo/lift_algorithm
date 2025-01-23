import tkinter as tk
import time
import json
import os
import multiprocessing
from multiprocessing import Queue



class ascenseur():
    
    def __init__(self,canvas,floor,queue,root,speed, Algorithm):
        ''' 
        Initialise the elevator object
        '''
        self.interrupt = False
        self.canvas = canvas
        self.root = root
        self.floor = 0
        self.algorithm = Algorithm()
        self.floors = [i for i in range(floor)]
        self.queue = queue
        self.speed = speed/floor
        self.floor_coords = []
        self.target_floors = []
        self.status = 0
        self.request_list = []
        canvas.update()
        n_stops = canvas.winfo_height()/floor
        height = canvas.winfo_height()
        for i in range(len(self.floors)+1):
            # Calculate the bottom of each floor
            bottom_coord = height - (i * n_stops)
            self.floor_coords.append(bottom_coord)
            canvas.create_line(0, bottom_coord, canvas.winfo_width(), bottom_coord, fill="black", width=2) #add line
            canvas.create_text(10, bottom_coord-(n_stops/2), text=str(i), fill="black", font=("Arial", 12, "bold")) #add floor label


        # Create object
        self.id = canvas.create_rectangle(
                                          40,
                                          self.floor_coords[0],
                                          40 + n_stops,
                                          self.floor_coords[0] - n_stops,
                                          fill='black'
                                          )

    def move_down(self,target_floor):
        ''' 
        This function takes as input the object and the target floor
        If the object is not at desired floor, move the lift down
        If the object is at desired floor, stop lift
        '''

        if self.interrupt:
            return
        
        self.status = 1 # Lift is active
        bottom_coords = self.canvas.coords(self.id)[3] # Current coords of bottom of lift
        target_coords = self.floor_coords[self.floors.index(target_floor)] # Get desired stop coord
        
        if bottom_coords < target_coords:
            self.canvas.move(self.id,0, self.speed) # Move object of self.speed down
            self.root.after(10, lambda: self.move_down(target_floor))
            
        else:
            self.request_list = list(filter(lambda x: x[0] != target_floor, self.request_list))
            time.sleep(1)
            self.status = 0 # Lift inactive
    
    def move_up(self,target_floor):
        ''' 
        This function takes as input the object and the target floor
        If the object is not at desired floor, move the lift up
        If the object is at desired floor, stop lift
        '''

        if self.interrupt:
            return
        
        self.status = 1
        bottom_coords = self.canvas.coords(self.id)[3] # Current coords of bottom of lift
        target_coords = self.floor_coords[self.floors.index(target_floor)] # Get desired stop coord


        if bottom_coords > target_coords:
            self.canvas.move(self.id,0, -self.speed) # Move object of self.speed up
            self.root.after(10, lambda: self.move_up(target_floor))
        else:
            self.request_list = list(filter(lambda x: x[0] != target_floor, self.request_list))
            time.sleep(1)
            self.status = 0

    def move(self):
        ''' 
        This function sends command to the lift making it go up or down 
        deppending on the list of target floors (requested floors)
        '''
        # Remove potential floors that do not exist
        for element in self.target_floors:
            if element not in self.floors:
                self.target_floors.remove(element)

        if self.interrupt:
            return

        # If lift is inactive: 
        if self.status == 0:
            # If floors in request list:
            if len(self.target_floors) > 0: 

                # If requested floor is higher than current position
                if self.target_floors[0] > self.floor:
                    # Request lift moves up to next floor in request list
                    self.move_up(self.target_floors.pop(0))

                # If requested floor is lower than current position
                elif self.target_floors[0] < self.floor:
                    # Request lift moves down to next floor in request list
                    self.move_down(self.target_floors.pop(0))
                
                # If requested floor equals current floor
                else: 
                    #Remove floor from request list
                    self.target_floors.pop(0)
        
        self.root.after(10, lambda: self.move())
        
    def update_floor(self):
        ''' 
        This function takes care of updating the current position of the lift,
        as well as outputing to the terminal the current floor each time it changes
        '''
        bottom_coords = self.canvas.coords(self.id)[3]
        
        # Check where the lift currently is located
        for i in range(len(self.floor_coords)):
            if bottom_coords <= self.floor_coords[i] and bottom_coords > self.floor_coords[i+1]:
                if self.floor == i:
                    pass
                else:
                    self.floor = i # Update object location
                    print(f"lift position: {self.floor}")

        self.root.after(50, self.update_floor)

    def interupt(self):
        self.interrupt = True
        self.target_floors = self.algorithm.system(self.request_list)
        self.interrupt = False
        self.move()

    def get_queue(self):
        while not self.queue.empty():
            request = self.queue.get()
            self.request_list.append(request)
            self.interupt()
        self.root.after(100,self.get_queue)

def get_input(queue: Queue, floors: list):
    ''' 
    Reads input from the terminal and adds requests to the lift's request list.
    '''
    directions = [1,0,-1]
    while True:
        user_input = input("enter desired floor and direction, expected format: floor,direction (direction = [-1,0,1])")
        if len(user_input.split(',')) != 2:
            print('wrong input, expected format: floor(int), direction(1,0,-1) i.e. 4,1')
            continue
        user_input = user_input.split(',')

        try:
            user_input[0] = int(user_input[0])
            user_input[1] = int(user_input[1])
        except ValueError:
            print('Floor and direction must be integers.')
            continue
        if user_input[0] not in floors:
            print('Floor not in list of floors')
            continue
        if user_input[1] not in directions:
            print('direction must be -1, 1 or 0')
            continue

        queue.put((user_input[0], user_input[1], time.time()))
        

def main_loop(floors, queue, speed, Algorithm):
    root = tk.Tk()
    root.title("Lift Simulation")
    canvas = tk.Canvas(root, width=800, height=1000, bg='white')
    canvas.pack()

    lift = ascenseur(canvas,floors,queue,root,speed, Algorithm)

    lift.get_queue()
    lift.update_floor()

    root.mainloop()

if __name__ == "__main__":

    with open(f"{os.path.dirname(__file__)}/config.json", "r") as file:
        config = json.load(file)
        floors = config["floors"]
        lifts = config["lifts"]
        speed = config["speed"]
        Algorithm = getattr(__import__(config["algorithm"]), "Algorithm")

    queue = Queue()
    
    multiprocessing.Process(target=main_loop, args=(floors, queue, speed, Algorithm,), daemon=True).start()

    get_input(queue, list(range(floors)))


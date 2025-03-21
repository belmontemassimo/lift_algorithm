import tkinter as tk
import time
import json
import os
import multiprocessing
from multiprocessing import Queue

''' 
To do:
- For automation:
    - Make sure the floors don't "re-input" the inside request
        - Create a second json file in which testing data gets temporarily transfered
        - Update inside request()
'''

class ascenseur():
    
    def __init__(self,canvas,floors,queue,root, Algorithm):
        ''' 
        Initialise the elevator object
        '''

        # Setup Object (lift)
        self.floor = 0
        self.status = 0
        self.interrupt = False
        self.algorithm = Algorithm()
        self.queue = queue
        # self.speed = int((floors*10)/50)
        self.speed = 1
        self.stops = []

        # Setup Building
        self.floors = [i for i in range(floors)]
        self.floor_coords = []

        # Setup Input methods
        self.target_floors = []
        self.request_list = []
        
        

        #  Setup tkinter
        canvas.update()
        self.canvas = canvas
        self.root = root
        n_stops = canvas.winfo_height()/floors
        height = canvas.winfo_height()
        for i in range(len(self.floors)+1):
            # Calculate the bottom of each floor
            bottom_coord = height - (i * n_stops)
            self.floor_coords.append(bottom_coord)
            canvas.create_line(0, bottom_coord, canvas.winfo_width(), bottom_coord, fill="black", width=2) #add line
            canvas.create_text(10, bottom_coord-(n_stops/2), text=str(i), fill="black", font=("Arial", 12, "bold")) #add floor label
        self.id = canvas.create_rectangle(
                                          40,
                                          self.floor_coords[0],
                                          40 + n_stops,
                                          self.floor_coords[0] - n_stops,
                                          fill='black'
                                          )

    def move_down(self,target_floor, request_element):
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
            self.canvas.move(self.id,0, 1) # Move object of self.speed down
            self.root.after(self.speed, lambda: self.move_down(target_floor, request_element))
            
        else:
            self.request_list = list(filter(lambda x: x[0] != target_floor, self.request_list))
            self.inside_request(target_floor,request_element)
            self.stops.append(target_floor)
            print(f"{len(self.stops)}: {self.stops}")
            # time.sleep(1)
            self.status = 0 # Lift inactive
    
    def move_up(self,target_floor, request_element):
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
            self.canvas.move(self.id,0, -1) # Move object of self.speed up
            self.root.after(self.speed, lambda: self.move_up(target_floor, request_element))
        else:
            self.request_list = list(filter(lambda x: x[0] != target_floor, self.request_list))
            self.inside_request(target_floor,request_element)
            self.stops.append(target_floor)
            print(f"{len(self.stops)}: {self.stops}")
            # time.sleep(1)
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
                    self.move_up(self.target_floors.pop(0),self.request_list.pop(0))
 

                # If requested floor is lower than current position
                elif self.target_floors[0] < self.floor:
                    # Request lift moves down to next floor in request list
                    self.move_down(self.target_floors.pop(0),self.request_list.pop(0))
      
                
                # If requested floor equals current floor
                else: 
                    #Remove floor from request list
                    self.target_floors.pop(0)
                    self.request_list.pop(0)

        
        self.root.after(200, lambda: self.move())
        
    def update_floor(self):
        ''' 
        This function takes care of updating the current position of the lift,
        as well as outputing to the terminal the current floor each time it changes
        '''
        lift_coords = (self.canvas.coords(self.id)[1] + self.canvas.coords(self.id)[3]) / 2
        
        # Check where the lift currently is located
        for i in range(len(self.floor_coords)):
            if lift_coords <= self.floor_coords[i] and lift_coords > self.floor_coords[i+1]:
                if self.floor == i:
                    pass
                else:
                    self.floor = i # Update object location
                    # print(f"lift position: {self.floor}")

        self.root.after(100, self.update_floor)

    def interupt(self):
        if len(self.request_list) == 0:
            return
        self.interrupt = True
        self.target_floors, self.request_list = self.algorithm.system(self.request_list)
        # print(self.target_floors)
        # print(self.request_list)
        self.interrupt = False
        self.move()

    def get_queue(self):
        while not self.queue.empty():
            request = self.queue.get()
            self.request_list.append(request)
        self.interupt()    
        self.root.after(100,self.get_queue)

    def inside_request(self,target_floor,request_element):

        '''
        to do:
            - make request_line go to other file after being used
        '''

        with open(f"{os.path.dirname(__file__)}/input_test.json", "r") as file:
            config = json.load(file)
            requests = config['test'] # List of lists with format: ["target_floor,direction", next_floor] 
            compatibility = f'{request_element[0]},{request_element[1]}'
            print(compatibility)

        new_set = []
        inside_request = None
        for request in requests: # find inside request and create new identical set without current target floor
            if compatibility == request[0]:
                inside_request = request[1] # next_floor
            else:
                new_set.append(request) 

        new_set = {'test': new_set}
    
        with open(f"{os.path.dirname(__file__)}/input_test.json", "w") as file:
            json.dump(new_set,file, indent=3)

        with open(f"{os.path.dirname(__file__)}/used_input_test.json", "r") as file:
            data = json.load(file)
            used_requests = data['test']
            used_requests_dict = {'test': used_requests}
        
        with open(f"{os.path.dirname(__file__)}/used_input_test.json", "w") as file:
            json.dump(used_requests_dict,file)

        if inside_request:
            self.queue.put((inside_request, 0, time.time()))   
            
                
                  
    def timer(self,start_time = None):
        if not start_time:
            start_time = time.time()

            if len(self.stops) != 21:
                self.root.after(100, lambda: self.timer(start_time=start_time))

            else: 
                stop_time = time.time()
                print(stop_time-start_time)
            

def get_input(queue: Queue, floors: list, method='json'):
    ''' 
    Reads input from the terminal and adds requests to the lift's request list.
    '''
    global fetched
    directions = [1,0,-1]

    while True:

        if method == 'json':
            if not fetched:
                with open(f"{os.path.dirname(__file__)}/input_test.json", "r") as file:
                    config = json.load(file)                
                    requests = config["test"]
           
                        
                    for request in requests:
                        if len(request[0].split(',')) != 2:
                            continue

                        request = request[0].split(',')

                        try:
                            request[0] = int(request[0])
                            request[1] = int(request[1])
                        except ValueError:
                            print('Floor and direction must be integers.')
                            continue
                        if request[0] not in floors:
                            print('Floor not in list of floors')
                            continue
                        if request[1] not in directions:
                            print('direction must be -1, 1 or 0')
                            continue

                        queue.put((request[0], request[1], time.time()))     
                    fetched = True
                
                    
        else:
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

def main_loop(floors, queue, Algorithm):
    root = tk.Tk()
    root.title("Lift Simulation")
    canvas = tk.Canvas(root, width=800, height=1000, bg='white')
    canvas.pack()

    lift = ascenseur(canvas,floors,queue,root, Algorithm)

    lift.timer()
    lift.get_queue()
    lift.update_floor()
    

    root.mainloop()



if __name__ == "__main__":

    with open(f"{os.path.dirname(__file__)}/config_template.json", "r") as file:
        config = json.load(file)
        floors = config["floors"]
        lifts = config["lifts"]
        Algorithm = getattr(__import__(config["algorithm"]), "Algorithm")

    queue = Queue()
    
    with open(f"{os.path.dirname(__file__)}/used_input_test.json", "r") as file:
        data = json.load(file)
    with open(f"{os.path.dirname(__file__)}/input_test.json", "w") as file:
        json.dump(data, file, indent=4)

    multiprocessing.Process(target=main_loop, args=(floors, queue, Algorithm,), daemon=True).start()

    fetched = False
    get_input(queue, list(range(floors)))
    


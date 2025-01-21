import tkinter as tk
import time

class ascenseur():
    
    def __init__(self,canvas,floor):
        ''' 
        Setup object, including:
        -current floor (0)
        -list of floors
        -speed of lift
        -y value of different floors
        -status of lift (0/1)
        '''
        self.canvas = canvas
        self.floor = 0
        self.floors = list()
        # Create list of floors
        for i in range(floor):
            self.floors.append(i)
        self.speed = 1
        self.floor_coords = []
        self.status = 0
        canvas.update()
        n_stops = canvas.winfo_height()/floors
        height = canvas.winfo_height()
        for i in range(len(self.floors)):
            # Calculate the bottom of each floor
            bottom_coord = height - (i * n_stops)
            self.floor_coords.append(bottom_coord)
            canvas.create_line(0, bottom_coord, canvas.winfo_width(), bottom_coord, fill="black", width=2) #add line
            canvas.create_text(10, bottom_coord-(n_stops/2), text=str(i), fill="black", font=("Arial", 12, "bold")) #add floor label
        self.floor_coords.append(0)

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
        self.status = 1 # Lift is active
        bottom_coords = canvas.coords(self.id)[3] # Current coords of bottom of lift
        target_coords = self.floor_coords[self.floors.index(target_floor)] # Get desired stop coord
        
        if bottom_coords < target_coords:
            canvas.move(self.id,0, self.speed) # Move object of self.speed down
            root.after(10, lambda: self.move_down(target_floor))
            
        else:
            time.sleep(1)
            self.status = 0 # Lift inactive
    
    def move_up(self,target_floor):
        ''' 
        This function takes as input the object and the target floor
        If the object is not at desired floor, move the lift up
        If the object is at desired floor, stop lift
        '''
        self.status = 1
        bottom_coords = canvas.coords(self.id)[3] # Current coords of bottom of lift
        target_coords = self.floor_coords[self.floors.index(target_floor)] # Get desired stop coord


        if bottom_coords > target_coords:
            canvas.move(self.id,0, -self.speed) # Move object of self.speed up
            root.after(10, lambda: self.move_up(target_floor))
        else:
            time.sleep(1)
            self.status = 0

    def move(self,target_floors):
        ''' 
        This function sends command to the lift making it go up or down 
        deppending on the list of target floors (requested floors)
        '''
        # Remove potential floors that do not exist
        for element in target_floors:
            if element not in self.floors:
                target_floors.remove(element)

        # If lift is inactive: 
        if self.status == 0:
            # If floors in request list:
            if len(target_floors) > 0: 

                # If requested floor is higher than current position
                if target_floors[0] > self.floor:
                    # Request lift moves up to next floor in request list
                    self.move_up(target_floors.pop(0))

                # If requested floor is lower than current position
                elif target_floors[0] < self.floor:
                    # Request lift moves down to next floor in request list
                    self.move_down(target_floors.pop(0))
                
                # If requested floor equals current floor
                else: 
                    #Remove floor from request list
                    target_floors.pop(0)

            else:
                return
        
        root.after(10, lambda: self.move(target_floors))
        
    def update_floor(self):
        ''' 
        This function takes care of updating the current position of the lift,
        as well as outputing to the terminal the current floor each time it changes
        '''
        bottom_coords = canvas.coords(self.id)[3]
        
        # Check where the lift currently is located
        for i in range(len(self.floor_coords)):
            if bottom_coords <= self.floor_coords[i] and bottom_coords > self.floor_coords[i+1]:
                if self.floor == i:
                    pass
                else:
                    self.floor = i # Update object location
                    print(f"lift position: {self.floor}")

        root.after(10, self.update_floor)

if __name__ == "__main__":
        
    root = tk.Tk()
    root.title("Lift Simulation")
    canvas = tk.Canvas(root, width=800, height=1000, bg='white')
    canvas.pack()
    floors = 50
    target_floors = [1,2,5,2,10,11,10,19,0]
    lift = ascenseur(canvas,floors)
    lift.move(target_floors)
    lift.update_floor()
    root.mainloop()

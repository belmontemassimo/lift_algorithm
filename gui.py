#
# file that contains all user interface logic
#

import tkinter as tk
from liftmanager import LiftManager
from lift import Lift

# nothing is implemented yet
class GUI:

    root: tk.Tk

    def __init__(self, n_floors: int, n_lifts: int, lift_manager:LiftManager):
        self.root = tk.Tk()
        self.root.title("GUI")

        # Create canvas
        self.canvas = tk.Canvas(self.root, width=800, height=1000, bg='white')
        self.canvas.pack()

        # Get dimensions
        self.root.update()
        n_stops = self.canvas.winfo_height()/n_floors
        height = self.canvas.winfo_height()
        
        # Add floors
        for i in range(n_floors+1):
            bottom_coord = height - (i * n_stops)
            self.canvas.create_line(0, bottom_coord, self.canvas.winfo_width(), bottom_coord, fill="black", width=2) #add line
            self.canvas.create_text(10, bottom_coord-(n_stops/2), text=str(i), fill="black", font=("Arial", 12, "bold")) #add floor label
        
        # Create lifts
        self.lifts = list()
        for i in range(1, (2*n_lifts) + 1):
            if i%2 == 1:
                self.lifts.append(self.canvas.create_rectangle(i*n_stops, height-n_stops, (i*n_stops)+n_stops, height, fill="black"))

        self.root.mainloop()
    
    def move(self, position):
        for i in range(len(self.lifts)):

            back_coords = None
            front_coords = self.canvas.coords(self.lifts[i])
            front_coords = front_coords[3] - front_coords[1]
            difference = None
            


            
    

a = GUI(20,1,lift_manager=0)
a.move()
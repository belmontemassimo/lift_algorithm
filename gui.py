#
# file that contains all user interface logic
#

import tkinter as tk
from multiprocessing import Process, Queue
from liftmanager import LiftManager


# nothing is implemented yet
class GUI:

    q: Queue
    root: tk.Tk


    def __init__(self, n_floors: int, n_lifts: int, q):
        self.q = q
        self.floors = n_floors
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


        self.root.after(1,self.queue_to_move)  # <-- CALL queue_to_move HERE

        self.root.mainloop()
    
    def queue_to_move(self):
        if not self.q.empty():  # Ensure there is data
            next_positions = self.q.get()
            self.move(next_positions)

        self.root.after(1, self.queue_to_move)  # Avoid recursion crash



        
    def move(self, positions):
        for i in range(len(self.lifts)):
            back_coords = positions[i]  # Target Y position
            self.canvas.update()
            front_coords = self.canvas.coords(self.lifts[i])  # Get lift rectangle coordinates
            
            current_y = front_coords[3]  # Use the bottom coordinate
            
            canvas_height = self.canvas.winfo_height()
            target_y = canvas_height - ((back_coords / self.floors) * canvas_height)  # Flip the coordinate system
            difference = target_y - current_y
            step = min(abs(difference), 5)  # Move at most 5 pixels per update

            if difference > 0:  # Move DOWN
                self.canvas.move(self.lifts[i], 0, step)
            elif difference < 0:  # Move UP
                self.canvas.move(self.lifts[i], 0, -step)

def run_gui(num_floors: int, num_lifts: int) -> Queue:
    gui_possition_queue: Queue = Queue()
    Process(target=GUI, args=(num_floors, num_lifts, gui_possition_queue)).start()
    return gui_possition_queue

def gui_update(lift_manager: LiftManager, gui_possition_queue: Queue):
    if gui_possition_queue.empty():
        gui_possition_queue.put(lift_manager.get_positions())
                


                
    


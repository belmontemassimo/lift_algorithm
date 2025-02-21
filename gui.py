#
# file that contains all user interface logic
#

import tkinter as tk
from multiprocessing import Process, Queue
from liftmanager import LiftManager


# nothing is implemented yet
class GUI:

    queue: Queue
    root: tk.Tk

    def __init__(self, n_floors: int, n_lifts: int, gui_queue):

        
        self.gui_queue:Queue = gui_queue

        # Fields 
        self.root = tk.Tk()
        self.root.title("GUI")
        self.canvas = tk.Canvas(self.root, width=800, height=1000, bg='white')
        self.canvas.pack()
        self.floors = n_floors
        self.lifts = list()
        self.seers = list()
        self.root.update()

        proportional_stops = self.canvas.winfo_height()/n_floors
        height = self.canvas.winfo_height()
        # Apply dimensions
        for i in range(n_floors+1):
            bottom_coord = height - (i * proportional_stops)
            self.canvas.create_line(0, bottom_coord, self.canvas.winfo_width(), bottom_coord, fill="black", width=2) #add line
            self.seers.append({'floor':i,'id':self.canvas.create_text(10, bottom_coord-(proportional_stops/2), text=str(i), fill="black", font=("Arial", 12, "bold")),'status':False}) #add floor label
        
        # Create lift objects
        for i in range(1, (2*n_lifts) + 1):
            if i%2 == 1:
                self.lifts.append(self.canvas.create_rectangle(i*proportional_stops, height-proportional_stops, (i*proportional_stops)+proportional_stops, height, fill="black"))

        # Call mainloop
        self.root.after(1,self.queue_manager)
        self.root.mainloop()
    
    def queue_manager(self):
        if not self.gui_queue.empty():  # Ensure there is data
            queue = self.gui_queue.get()
            next_positions = queue['positions']
            current_targets = queue['targets']
        
            self.move(next_positions)
            self.seers_update(current_targets)

        self.root.after(1, self.queue_manager)  # Avoid recursion crash


    def move(self, positions):
        for i in range(len(self.lifts)):
            back_coords = positions[i]  # Target Y position
            self.canvas.update()
            front_coords = self.canvas.coords(self.lifts[i])  # Get lift rectangle coordinates
            
            current_y = front_coords[3]  # Use the bottom coordinate
            
            canvas_height = self.canvas.winfo_height()
            target_y = canvas_height - ((back_coords / self.floors) * canvas_height)  # Flip the coordinate system
            difference = target_y - current_y
            step = abs(difference)

            if difference > 0:  # Move DOWN
                self.canvas.move(self.lifts[i], 0, step)
            elif difference < 0:  # Move UP
                self.canvas.move(self.lifts[i], 0, -step)

    def seers_update(self,current_targets):
        for seer in self.seers:

            if seer['floor'] in current_targets and seer['status'] == False:
                self.canvas.itemconfig(seer['id'], fill='red')
                seer['status'] = True
            
            elif seer['floor'] not in current_targets and seer['status'] == True:
                self.canvas.itemconfig(seer['id'], fill='black')
                seer['status'] = False
            
            else:
                continue

def run_gui(num_floors: int, num_lifts: int) -> Queue:
    gui_queue: Queue = Queue()

    Process(target=GUI, args=(num_floors, num_lifts, gui_queue)).start()
    return gui_queue

def gui_update(lift_manager: LiftManager, gui_queue: Queue):
    if gui_queue.empty():
        gui_queue.put({'positions':lift_manager.get_positions(), 'targets':lift_manager.get_target_floors()})

                
    


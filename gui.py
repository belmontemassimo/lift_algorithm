#
# file that contains all user interface logic
#

import tkinter as tk
from multiprocessing import Process, Queue
from liftmanager import LiftManager


# Lift colors
COLORS = [
    "#1C2526",  # Dark Slate Gray
    "#3C2F2F",  # Dark Brown
    "#4A4A4A",  # Dark Gray
    "#2F1C0F",  # Deep Coffee Brown
    "#3F2A44",  # Dark Plum
    "#1A3C34",  # Dark Teal
    "#5C4033",  # Dark Sienna
    "#2B1D3A",  # Dark Indigo
    "#2E2E2E",  # Charcoal Gray
    "#403530",  # Dark Taupe
    "#1F2F3C",  # Dark Steel Blue
    "#3A2A29"   # Dark Mahogany
]

# Lift shadows' colors
TRANSPARENT_COLORS = [
    "#788081",  # Lightened Slate Gray
    "#8D7F7F",  # Lightened Brown
    "#989898",  # Lightened Gray
    "#847873",  # Lightened Coffee Brown
    "#8E7C91",  # Lightened Plum
    "#778D88",  # Lightened Teal
    "#A28E85",  # Lightened Sienna
    "#837588",  # Lightened Indigo
    "#858585",  # Lightened Charcoal Gray
    "#908784",  # Lightened Taupe
    "#7A858C",  # Lightened Steel Blue
    "#8B7C7B"   # Lightened Mahogany
]


class GUI:

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
        self.shadow_lifts = list()
        proportional_stops = self.canvas.winfo_height()/n_floors  # Distance between floors
        height = self.canvas.winfo_height()

        # Apply dimensions
        for i in range(n_floors+1):
            bottom_coord = height - (i * proportional_stops)
            self.canvas.create_line(0, bottom_coord, self.canvas.winfo_width(), bottom_coord, fill="black", width=2) #add line
            self.seers.append({'floor':i,'id':self.canvas.create_text(10, bottom_coord-(proportional_stops/2), text=str(i), fill="black", font=("Arial", 12, "bold")),'status':False}) #add floor label
        
        # Create lift objects and their shadows
        for i in range(1, (2*n_lifts) + 1):
            if i%2 == 1:
                lift_color = COLORS[int(((i-1)/2)%len(COLORS))]
                shadow_color = TRANSPARENT_COLORS[int(((i-1)/2)%len(TRANSPARENT_COLORS))]
                self.shadow_lifts.append(self.canvas.create_rectangle(i*proportional_stops, height-proportional_stops, (i*proportional_stops)+proportional_stops, height, fill=shadow_color, outline=shadow_color))
                self.lifts.append(self.canvas.create_rectangle(i*proportional_stops, height-proportional_stops, (i*proportional_stops)+proportional_stops, height, fill=lift_color))

        # Call mainloop
        self.root.after(1,self.queue_manager)
        self.root.mainloop()
    

    def queue_manager(self):
        # Get data from queue and call functions shadow movement, move and seers_update accordingly

        if not self.gui_queue.empty():  # Ensure there is data
            queue = self.gui_queue.get()
            next_positions = queue['positions']  # Current lift positions
            current_targets = queue['targets']   # Target floors for lifts

            self.shadow_movements(current_targets) # Move shadow to target floor
            self.move(next_positions) # Move lift to current position
            self.seers_update(current_targets) # Change seers colors

        self.root.after(1, self.queue_manager)  # Avoid recursion crash


    def shadow_movements(self, current_targets):
        # Move shadow lifts to preview target floors or align with idle lifts
        for i, target in enumerate(current_targets):
            
            if target:  # If lift has a target floor
                self.canvas.update()
                front_coords = self.canvas.coords(self.shadow_lifts[i])  # Get lift rectangle coordinates
                current_y = front_coords[3]  # Use the bottom coordinate x1,y1,x2,y2)
                
                canvas_height = self.canvas.winfo_height()
                target_y = canvas_height - ((target / self.floors) * canvas_height)  # Flip the coordinate system
                difference = target_y - current_y
                step = abs(difference)

                if difference > 0:  # Move DOWN
                    self.canvas.move(self.shadow_lifts[i], 0, step)
                elif difference < 0:  # Move UP
                    self.canvas.move(self.shadow_lifts[i], 0, -step)
            
            else: # If no target floor, lift shadow goes same coordinates as corresponding lift
                lift_coords = self.canvas.coords(self.lifts[i])[3]
                shadow_lift_coords = self.canvas.coords(self.shadow_lifts[i])[3]
                if lift_coords != shadow_lift_coords:
                    difference = lift_coords - shadow_lift_coords
                    self.canvas.move(self.shadow_lifts[i],0, difference)



    def move(self, positions):
        # Move lifts to their current positions from LiftManager
        for i in range(len(self.lifts)):
            back_coords = positions[i]  # Target Y position
            self.canvas.update()
            front_coords = self.canvas.coords(self.lifts[i])  # Get lift rectangle coordinates
            
            current_y = front_coords[3]  # Use the bottom coordinate x1,y1,x2,y2)
            
            canvas_height = self.canvas.winfo_height()
            target_y = canvas_height - ((back_coords / self.floors) * canvas_height)  # Flip the coordinate system
            difference = target_y - current_y
            step = abs(difference)

            if difference > 0:  # Move DOWN
                self.canvas.move(self.lifts[i], 0, step)
            elif difference < 0:  # Move UP
                self.canvas.move(self.lifts[i], 0, -step)

    def seers_update(self,current_targets):
        # Update floor labels (seers) to reflect target activity
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
    # Start GUI in a separate process and return queue for communication
    gui_queue: Queue = Queue()

    Process(target=GUI, args=(num_floors, num_lifts, gui_queue)).start()
    return gui_queue

def gui_update(lift_manager: LiftManager, gui_queue: Queue):
    # Send lift positions and targets to GUI via queue
    if gui_queue.empty():
        gui_queue.put({'positions':lift_manager.get_positions(), 'targets':lift_manager.get_target_floors()})
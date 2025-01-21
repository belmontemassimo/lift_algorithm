import tkinter as tk
import time

class ascenseur():
    
    def __init__(self,canvas,floors):
        self.canvas = canvas
        self.floor = min(floors)
        self.floors = floors
        self.speed = 1
        self.floor_coords = []
        self.calls = []
        self.status = 0
        canvas.update()
        n_stops = canvas.winfo_height()/len(floors)
        height = canvas.winfo_height()
        for i in range(len(floors)):
            # Calculate the bottom of each floor
            bottom_coord = height - (i * n_stops)
            self.floor_coords.append(bottom_coord)
            canvas.create_line(0, bottom_coord, canvas.winfo_width(), bottom_coord, fill="black", width=2)
            canvas.create_text(10, bottom_coord, text=str(i+1), fill="black", font=("Arial", 12, "bold"))



        self.floor_coords.append(0)

        self.id = canvas.create_rectangle(self.floor_coords[0],self.floor_coords[0],self.floor_coords[0]-40,self.floor_coords[0]-40,fill='black')
        print(self.floor_coords)
        print(self.floors)

    def move_down(self,target_floor):
        self.status = 1
        bottom_coords = canvas.coords(self.id)[3]
        target_coords = self.floor_coords[self.floors.index(target_floor)]
        
        if bottom_coords < target_coords:
            canvas.move(self.id,0, self.speed)
            root.after(10, lambda: self.move_down(target_floor))
            
        else:
            time.sleep(2)
            self.status = 0
    
    def move_up(self,target_floor):
        self.status = 1
        bottom_coords = canvas.coords(self.id)[3]
        target_coords = self.floor_coords[self.floors.index(target_floor)]

        if bottom_coords > target_coords:
            canvas.move(self.id,0, -self.speed)
            root.after(10, lambda: self.move_up(target_floor))
        else:
            time.sleep(2)
            self.status = 0

    def move(self,target_floors):
            for element in target_floors:
                if element not in self.floors:
                    target_floors.remove(element)
            
            if self.status == 0:
                if len(target_floors) > 0:

                    if target_floors[0] > self.floor:
                        self.move_up(target_floors.pop(0))

                    elif target_floors[0] < self.floor:
                        self.move_down(target_floors.pop(0))
                        
                    else:
                        target_floors.pop(0)
            
            
            root.after(10, lambda: self.move(target_floors))
            
    def update_floor(self):
        bottom_coords = canvas.coords(self.id)[3]
        for i in range(len(self.floor_coords)):
            if bottom_coords <= self.floor_coords[i] and bottom_coords > self.floor_coords[i+1]:
                if self.floor == i+1:
                    pass
                else:
                    self.floor = i+1
                    print(f"lift position: {self.floor}")

        root.after(10, self.update_floor)

if __name__ == "__main__":    
    root = tk.Tk()
    canvas = tk.Canvas(root, width=800, height=600, bg='white')
    canvas.pack()
    floors = [1,2,3,4,5,6,7,8,9,10]
    target_floors = [10,1]
    lift = ascenseur(canvas,floors)
    lift.move(target_floors)
    lift.update_floor()
    root.mainloop()

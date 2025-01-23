'''
PLACEHOLDER FOR THE SIMULATION FOR TESTING PURPOSES!!!!!
'''
class FloorRequest:
    def __init__(self, floors):
        self.floors = floors

    def get_floors(self):
        return self.floors


class LOOK:
    '''	
    Look algorithm that returns an ordered lift for the lift simulation to work with.
    Gets a list from the lift system simulation and sends it back.
    '''
    def __init__(self, current_floor=0):
        '''	
        Needs the current floor to determine whether to go up or down based on the number 
        of items in the list in front or behind the current floor
        '''
        self.current_floor = current_floor

    def system(self, floor_request):
        floors = floor_request.get_floors()#SHOULD BE CHANGED TO GET FLOORS FROM SIMULATION WHEN READY
        floors.sort() #sorts the list of floors
        #once the list is sorted, the algorithm will look for the current floor and then go up and down
        up = [floor for floor in floors if floor >= self.current_floor]
        down = [floor for floor in floors if floor < self.current_floor]
        #makes a new list for the floors that are ordered in the most efficient way
        ordered_floors = up + down[::-1]
        #ordered list will be send back to the ascenseur class
        return ordered_floors


'''
TO BE CHANGED LATER, ORDERED FLOORS WILL BE USED BY THE SIMULATION!!!!!
'''	
if __name__ == "__main__":
    floor_request = FloorRequest([10, 1, 2, 2, 5, 6, 7, 8, 9, 10, 0, 3, 5])
    lift_system = LOOK(current_floor=3)
    ordered_floors = lift_system.system(floor_request)
    print("Ordered floors:", ordered_floors)
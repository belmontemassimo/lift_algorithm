class Algorithm:
    def __init__(self):
        pass

    def system(self, request_list):
        # Initialize an output list to store floor numbers
        
        floors = []
        
        # Extract floor numbers from the request_list
        for element in request_list:
            floor = element[0]
            floors.append(floor)

        return floors, request_list
        # zipped_list = zip(floors,request_list)
        # zipped_list = sorted(zipped_list)
        
        # floors, request_list = zip(*zipped_list) 

        # return list(floors), list(request_list)

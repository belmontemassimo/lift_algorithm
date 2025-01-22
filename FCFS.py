class Algorithm():
    def __init__(self):
        pass
    def system(self,request_list):
        # request_list = [(1,1,time),(2,1,time),(3,1,time),(2,1,time)]
        output = []
        for element in request_list:
            output.append(element[0])

        return request_list,output
    
    # output: [(1,1,time),(2,1,time),(3,1,time),(2,1,time)], [1,2,3,2]

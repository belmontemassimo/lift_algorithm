from request import Request
from extenders import double_normal_distribution
from os import path, makedirs
from random import randint
from os import listdir
from os.path import isdir, exists
from json import dump, loads


if __name__ == "__main__":
    # Check if the samples directory exists and create it if not
    if not path.exists("./samples"):
        makedirs("./samples")  # Create the samples directory if it doesn't exist

    # Initialize a list to hold request dictionaries and gather user inputs
    requests: list[dict[str,int]] = []
    max_floor: int = int(input("max_floor: "))  
    num_requests: int = int(input("num_requests: "))  
    total_time: int = int(input("total_time: "))  

    # Validate user inputs and exit if they are incorrect
    if max_floor <= 1 or num_requests <= 0 or total_time <= 0:
        print("incorrect inputs")  
        exit()  

    # Loop to generate requests based on user-defined parameters
    while True:
        request_floor = randint(0, max_floor)  
        target_floor = randint(0, max_floor)  
        created_time = randint(0, total_time)  
        weight_captor = int(double_normal_distribution() * 100) 

        # Only add the request if the request floor is different from the target floor
        if request_floor != target_floor:
            requests.append({"request_floor": request_floor, "target_floor": target_floor, "created_time": created_time, "weight_captor": weight_captor})
            if len(requests) == num_requests - 1:  
                break

    # List all existing sample files in the samples directory
    all_samples = listdir("./samples")

    # Loop to find a unique sample file name for saving
    sample_number = 1  
    while True:
        if f"sample_{sample_number}" in all_samples:  
            sample_number += 1  
            continue
        # Open a new sample file for writing and save the requests
        with open(f"./samples/sample_{sample_number}", "w") as file:
            dump(sorted(requests, key=lambda request: request["created_time"]), file)  # Save requests sorted by creation time
            break  

    # Print confirmation of saved sample
    print(f"saved as sample_{sample_number}")  

# Function to convert a request dictionary to a Request object
def dict_to_request(request_dict: dict[str,int]):
    return Request(request_dict["request_floor"], request_dict["target_floor"], request_dict["created_time"], request_dict["weight_captor"])

# returns the sample file if it exists
def samples_list() -> list[str]:
    if isdir("./samples"):
        return listdir("./samples")
    return []

# load the sample file to a list containing the requests
def load_sample(file_name: str) -> list[Request]:
    if exists(f"./samples/{file_name}"):
        with open(f"./samples/{file_name}", "r") as file:
            return [dict_to_request({key: value for key, value  in request_dict.items()}) for request_dict in loads(file.read())]
    return []

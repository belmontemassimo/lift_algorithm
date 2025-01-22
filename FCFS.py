class Algorithm:
    def __init__(self, elevator):
        """
        Initialize the algorithm.

        Parameters:
        - elevator: An instance of the 'ascenseur' class.
        """
        self.elevator = elevator  # Reference to the elevator object
        self.request_queue = []   # List to store floor requests
        self.processing = False   # Flag to indicate if processing is active

    def system(self, floor):
        """
        Add a floor request to the queue.

        Parameters:
        - floor: Floor number to add to the queue.
        """
        if floor not in self.request_queue:  # Avoid duplicate requests
            self.request_queue.append(floor)
            print(f"Request added: Floor {floor}")
        
        # Start processing if not already active
        if not self.processing:
            self.process_requests(self.FCFS)

    def process_requests(self, algorithm):
        """
        Process requests using the specified algorithm.

        Parameters:
        - algorithm: The algorithm method to use (e.g., self.FCFS).
        """
        if self.request_queue and not self.processing:
            self.processing = True
            algorithm()  # Call the specified algorithm method
        else:
            print("No requests to process or already processing.")

    def FCFS(self):
        """
        Implements the First Come First Serve (FCFS) algorithm.
        """
        if self.request_queue:
            next_floor = self.request_queue.pop(0)  # Get the next request
            print(f"FCFS: Moving to floor {next_floor}")
            self.elevator.move([next_floor])  # Command the elevator to move
        else:
            self.processing = False
            print("All requests completed.")

    def on_reach_floor(self):
        """
        Callback for when the elevator reaches a floor.
        """
        print(f"Elevator reached floor {self.elevator.floor}")
        self.processing = False  # Allow processing of the next request
        self.process_requests(self.FCFS)  # Continue with the next request

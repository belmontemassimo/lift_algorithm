class LiftSystem:
    def __init__(self, initial_floor=0):
        self.current_floor = initial_floor
        self.requests = []

    def request_floor(self, floor):
        self.requests.append(floor)
        print(f"Floor {floor} requested.")

    def run(self):
        while self.requests:
            next_floor = self.requests.pop(0)
            self.move_to_floor(next_floor)

    def move_to_floor(self, floor):
        print(f"Moving from floor {self.current_floor} to floor {floor}.")
        self.current_floor = floor
        print(f"Arrived at floor {floor}.")

if __name__ == "__main__":
    lift = LiftSystem()
    lift.request_floor(3)
    lift.request_floor(1)
    lift.request_floor(5)
    lift.run()
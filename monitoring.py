from wx import App, Frame, StaticText, Panel, TextCtrl, Button, Choice, Timer
from wx import EVT_BUTTON, EVT_TIMER
from lift import LiftState
from multiprocessing import Process, Queue
from liftmanager import LiftManager

class Monitoring:

    app: App
    frame: Frame
    panel: Panel
    position_label: StaticText
    speed_label: StaticText
    state_label: StaticText
    weight_label: StaticText
    target_floor: StaticText
    speed_input: TextCtrl
    speed_text: StaticText
    lift_number_input: TextCtrl
    lift_number_text: StaticText
    num_floors_input: TextCtrl
    num_floors_text: StaticText
    start_button: Button
    timer_text: StaticText
    algorithm_choice: Choice
    queue: Queue
    algorithms: dict[str, object]
    capacity: int
    timer: Timer

    def __init__(self, queue: Queue, algorithms: dict[str, object], capacity: int):
        self.queue = queue
        self.capacity = capacity
        self.algorithms = algorithms
        self.app = App()
        self.frame = Frame(parent=None, title='Monitoring')
        self.panel = Panel(self.frame, -1)
        self.position_label = StaticText(self.panel, -1, "", (25, 25))
        self.speed_label = StaticText(self.panel, -1, "", (25, 45))
        self.state_label = StaticText(self.panel, -1, "", (25, 65))
        self.weight_label = StaticText(self.panel, -1, "", (25, 85))
        self.timer_text = StaticText(self.panel, -1, "", (25, 125))
        self.target_floor = StaticText(self.panel, -1, "", (25, 105))
        self.speed_input = TextCtrl(self.panel, -1, "1", (250,55), (50,20))
        self.speed_text = StaticText(self.panel, -1, "speed", (315, 55), (70,20))
        self.lift_number_input = TextCtrl(self.panel, -1, "1", (250,85), (50,20))
        self.lift_number_text = StaticText(self.panel, -1, "lifts", (315, 85), (70,20))
        self.num_floors_input = TextCtrl(self.panel, -1, "10", (250,115), (50,20))
        self.num_floors_text = StaticText(self.panel, -1, "floors", (315, 115), (70,20))
        self.start_button = Button(self.panel, -1, "start", (280, 145), (100,20))
        self.start_button.Bind(EVT_BUTTON, self.on_start_update)
        self.algorithm_choice = Choice(self.panel, -1, (280,25), (100,20), self.algorithms)
        self.timer = Timer(self.frame)
        self.frame.Bind(EVT_TIMER, self.update, self.timer)
        self.frame.Show()
        self.app.MainLoop()

    def update(self, _):
        if self.queue.empty():
            return
        data: dict = self.queue.get()
        self.position_label.SetLabelText(f'position:      {" ".join(["%.2f" % item for item in  data["positions"]])}')
        self.speed_label.SetLabelText(f'speed:         {" ".join(["%.2f" % item for item in data["speed"]])}')
        self.state_label.SetLabelText(f'state:         {" ".join(["W" if state == LiftState.WAITING else "I" if state == LiftState.IDLE else "M" for state in data["states"]])}')
        self.weight_label.SetLabelText(f'weight:        {" ".join(["%.1f" % item for item in  data["weight"]])} / {"%.1f" % self.capacity}')
        self.target_floor.SetLabelText(f'target floor:  {" ".join(["%.1f" % item for item in data["target_floors"]])}')
        self.timer_text.SetLabelText(f'time:  {"%.2f" % data["timer"]}')

    def on_start_update(self, _):
        try:
            self.queue.put({
                "lifts": int(self.lift_number_input.GetValue()),
                "time": float(self.speed_input.GetValue()),
                "floors": int(self.num_floors_input.GetValue()),
                "algorithm": self.algorithm_choice.GetString(self.algorithm_choice.GetSelection())
            })
            self.algorithm_choice.Disable()
            self.start_button.Disable()
            self.speed_input.Disable()
            self.lift_number_input.Disable()
            self.num_floors_input.Disable()
            self.speed_text.Disable()
            self.lift_number_text.Disable()
            self.num_floors_text.Disable()
        except:
            return

        while True:
            if self.queue.empty():
                break
        self.timer.Start(40)

def run_monitoring(algorithms: dict[str, object], capacity: int) -> Queue:
    queue = Queue()
    Process(target=Monitoring, args=[queue, algorithms, capacity]).start()
    return queue

def update_monitoring(queue: Queue, lift_manager: LiftManager, timer: float):
    if queue.empty():
        lifts = lift_manager.lifts
        data = {
            "positions": [lift.position for lift in lifts],
            "speed": [lift.speed for lift in lifts],
            "states": [lift.state for lift in lifts],
            "weight": [lift.weight/100 for lift in lifts],
            "target_floors": [lift.target_floor for lift in lifts],
            "timer": timer,
        }
        queue.put(data)
    return 

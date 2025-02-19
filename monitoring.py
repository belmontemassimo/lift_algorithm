from wx import App, Frame, StaticText, Panel, TextCtrl, Button, Choice
from wx import EVT_BUTTON
from liftmanager import LiftManager
from lift import LiftState
from algorithms import AlgorithmHandler
from extenders import set_time_multiplier, set_number_of_lifts, start_simulation, set_number_of_floors

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
    timer: StaticText
    algorithm_choice: Choice
    lift_manager: LiftManager
    algorithm: AlgorithmHandler

    def __init__(self, lift_manager: LiftManager, algorithm: AlgorithmHandler):
        self.lift_manager = lift_manager
        self.algorithm = algorithm
        self.app = App()
        self.frame = Frame(parent=None, title='Monitoring')
        self.panel = Panel(self.frame, -1)
        self.position_label = StaticText(self.panel, -1, "", (25, 25))
        self.speed_label = StaticText(self.panel, -1, "", (25, 45))
        self.state_label = StaticText(self.panel, -1, "", (25, 65))
        self.weight_label = StaticText(self.panel, -1, "", (25, 85))
        self.timer = StaticText(self.panel, -1, "", (25, 125))
        self.target_floor = StaticText(self.panel, -1, "", (25, 105))
        self.speed_input = TextCtrl(self.panel, -1, "1", (250,55), (50,20))
        self.speed_text = StaticText(self.panel, -1, "speed", (315, 55), (70,20))
        self.lift_number_input = TextCtrl(self.panel, -1, "1", (250,85), (50,20))
        self.lift_number_text = StaticText(self.panel, -1, "lifts", (315, 85), (70,20))
        self.num_floors_input = TextCtrl(self.panel, -1, "10", (250,115), (50,20))
        self.num_floors_text = StaticText(self.panel, -1, "floors", (315, 115), (70,20))
        self.start_button = Button(self.panel, -1, "start", (280, 145), (100,20))
        self.start_button.Bind(EVT_BUTTON, self.on_start_update)
        self.algorithm_choice = Choice(self.panel, -1, (280,25), (100,20), self.algorithm.get_list())
        self.frame.Show()

    def update(self, timer:float):
        if self.lift_manager:
            self.position_label.SetLabelText(f'position:      {" ".join(["%.2f" % item for item in  self.lift_manager.get_positions()])}')
            self.speed_label.SetLabelText(f'speed:         {" ".join(["%.2f" % item for item in self.lift_manager.get_speed()])}')
            self.state_label.SetLabelText(f'state:         {" ".join(["W" if state == LiftState.WAITING else "I" if state == LiftState.IDLE else "M" for state in self.lift_manager.get_states()])}')
            self.weight_label.SetLabelText(f'weight:        {" ".join(["%.1f" % item for item in  self.lift_manager.get_weight_kg()])} / {"%.1f" % self.lift_manager.capacity}')
            self.target_floor.SetLabelText(f'target floor:  {" ".join(["%.1f" % item for item in self.lift_manager.get_target_floors()])}')
            self.timer.SetLabelText(f'time:  {"%.2f" % timer}')
        self.app.Yield()

    def on_start_update(self, _):
        try:
            set_number_of_lifts(int(self.lift_number_input.GetValue()))
            set_time_multiplier(float(self.speed_input.GetValue()))
            set_number_of_floors(int(self.num_floors_input.GetValue()))
            self.algorithm.set_algorithm(self.algorithm_choice.GetString(self.algorithm_choice.GetSelection()))
            start_simulation()
            self.algorithm_choice.Disable()
            self.start_button.Disable()
        except:
            return

from wx import App, Frame, StaticText, Panel, TextCtrl, Button, Choice
from wx import EVT_BUTTON, EVT_CHOICE
from liftmanager import LiftManager
from lift import LiftState
from algorithms import AlgorithmHandler
from extenders import set_time_multiplier, get_time_multiplier

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
    speed_button: Button
    timer: StaticText
    algorithm_choice: Choice
    lift_manager: LiftManager
    algorithm: AlgorithmHandler

    def __init__(self, lift_manager: LiftManager, algorithm: AlgorithmHandler):
        set_time_multiplier(0)
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
        self.speed_input = TextCtrl(self.panel, -1, "1", (220,55), (50,20))
        self.speed_button = Button(self.panel, -1, "update", (285, 55), (70,20))
        self.speed_button.Bind(EVT_BUTTON, self.on_speed_update)
        self.algorithm_choice = Choice(self.panel, -1, (250,25), (100,20), self.algorithm.get_list())
        self.algorithm_choice.Bind(EVT_CHOICE, self.on_algorithm_choice)
        self.frame.Show()

    def update(self, timer:float):
        state = self.lift_manager.get_states()[0]
        self.position_label.SetLabelText(f'position:      {"%.2f" % self.lift_manager.get_positions()[0]}')
        self.speed_label.SetLabelText(f'speed:         {"%.2f" % self.lift_manager.get_speed()[0]}')
        self.state_label.SetLabelText(f'state:         {"waiting" if state == LiftState.WAITING else "idle" if state == LiftState.IDLE else "moving"}')
        self.weight_label.SetLabelText(f'weight:        {"%.2f" % self.lift_manager.get_weight_kg()[0]}/{"%.2f" % self.lift_manager.capacity}')
        self.target_floor.SetLabelText(f'target floor:  {"%.2f" % self.lift_manager.get_target_floors()[0]}')
        self.timer.SetLabelText(f'time:  {"%.2f" % timer}')
        self.app.Yield()

    def on_speed_update(self, _):
        try:
            set_time_multiplier(float(self.speed_input.GetValue()))
            return
        except:
            return
        
    def on_algorithm_choice(self, _):
        self.algorithm.set_algorithm(self.algorithm_choice.GetString(self.algorithm_choice.GetSelection()))
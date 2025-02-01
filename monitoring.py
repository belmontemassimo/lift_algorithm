from wx import App, Frame, StaticText, Panel
from liftmanager import LiftManager
from lift import LiftState

class Monitoring:

    app: App
    frame: Frame
    panel: Panel
    position_label: StaticText
    speed_label: StaticText
    state_label: StaticText
    weight_label: StaticText
    target_floor: StaticText
    timer: StaticText
    lift_manager: LiftManager

    def __init__(self, lift_manager: LiftManager):
        self.lift_manager = lift_manager
        self.app = App()
        self.frame = Frame(parent=None, title='Monitoring')
        self.panel = Panel(self.frame, -1)
        self.position_label = StaticText(self.panel, -1, "", (25, 25))
        self.speed_label = StaticText(self.panel, -1, "", (25, 45))
        self.state_label = StaticText(self.panel, -1, "", (25, 65))
        self.weight_label = StaticText(self.panel, -1, "", (25, 85))
        self.target_floor = StaticText(self.panel, -1, "", (25, 105))
        self.timer = StaticText(self.panel, -1, "", (25, 125))
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
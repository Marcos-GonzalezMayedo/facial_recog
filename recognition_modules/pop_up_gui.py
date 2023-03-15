import simple_gui
import PySimpleGUI as sg

#Requires a question for which to query the user:
class pop_up_gui(simple_gui.simple_gui):
    def __init__(self, layout: list):
        super().__init__(layout)

    def get_window_events(self):
        return super().getWindow().read()
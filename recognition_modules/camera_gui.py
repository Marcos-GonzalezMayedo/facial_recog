import PySimpleGUI as sg
import simple_gui

class camera_gui(simple_gui.simple_gui):
    def __init__(self, layout = [
            [sg.Text("Camera View", size=(60,1), justification='center'),
            sg.Button("Capture", size=(10,1), button_color='red'), sg.Button("Exit", 
            size=(10, 1), button_color='red')],
            [sg.Image(filename='', key="image",size=(500, 300))],
        ]):
        sg.theme('DarkAmber')
        super().__init__(layout)

    def setGuiImage(self, image):
        window = super().getWindow()
        window["image"].update(data=image)

    def checkEvent(self):
        window = super().getWindow()
        return window.read(20)

    
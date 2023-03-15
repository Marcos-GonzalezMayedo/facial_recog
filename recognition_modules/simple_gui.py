import PySimpleGUI as sg

class simple_gui:
    def __init__(self, layout):
        self.layout = layout
    
    def display(self):
        self.window = sg.Window("Simple Gui", self.layout, size=(1200, 800), finalize=True)

    def getLayout(self):
        return self.layout

    def getWindow(self):
        return self.window

    def killWindow(self):
        self.window.close()
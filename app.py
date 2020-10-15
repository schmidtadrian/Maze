import tkinter as tk
import config as cfg
from settings import SettingsBar
from maze import Maze

class MainApplication(tk.Frame):
    """ This class is the toplevel window which integrates Settingsbar and Maze in the frame"""
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        self.parent       = parent
        self.maze         = None
        self.settings_bar = SettingsBar(self)
        self.settings_bar.pack()

    
if __name__ == "__main__":
    """ Application entry point """
    root = tk.Tk()
    root.title(cfg.WINDOW_TITLE)
    MainApplication(root).pack()
    root.mainloop()
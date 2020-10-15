import tkinter as tk
import tkinter.messagebox
import config as cfg
from maze import Maze

class SettingsBar(tk.LabelFrame):
    """ This class handles all UI Elements execpt the maze canvas """
    
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text = "Settings")
        
        self.parent     = parent
        self.show_grid  = tk.BooleanVar(value = cfg.DEFAULT_SHOW_GRID)

        # Create widget instances        
        self.columns_label         = tk.Label      (self, text = "Width [Cells]:" )
        self.rows_label            = tk.Label      (self, text = "Height [Cells]:")
        self.animation_speed_label = tk.Label      (self, text = "Animation speed")
        self.show_grid_label       = tk.Label      (self, text = "Show grid"      )
        self.columns_entry         = tk.Entry      (self, width = 16)
        self.rows_entry            = tk.Entry      (self, width = 16)
        self.generate_maze_button  = tk.Button     (self, text = "Generate maze",                      command = self.generate_maze)
        self.solve_maze_button     = tk.Button     (self, text = "Solve maze"   , state = tk.DISABLED, command = self.solve_maze)
        self.animation_speed_scale = tk.Scale      (self, from_ = 200, to = 0, showvalue = 0, resolution = 1, orient = tk.HORIZONTAL, command = self.set_animation_delay)
        self.show_grid_checkbutton = tk.Checkbutton(self, var = self.show_grid)

        # Align widgets
        self.columns_label.grid        (row = 0, column = 0, sticky = "e"            )
        self.columns_entry.grid        (row = 0, column = 1                          )
        self.rows_label.grid           (row = 1, column = 0, sticky = "e"            )
        self.rows_entry .grid          (row = 1, column = 1                          )
        self.generate_maze_button.grid (row = 0, column = 2                          )
        self.solve_maze_button.grid    (row = 1, column = 2, sticky = "ew"           )
        self.animation_speed_label.grid(row = 0, column = 3, sticky = "ew", padx = 10)
        self.animation_speed_scale.grid(row = 1, column = 3,                padx = 10)
        self.show_grid_label.grid      (row = 0, column = 4                          )
        self.show_grid_checkbutton.grid(row = 1, column = 4, sticky = "new"          )

        # Set scale to default animation delay
        self.animation_speed_scale.set(cfg.ANIMATION_DELAY)
    
    def set_animation_delay(self, e):
        """ Called by animation speed scale to set animation speed/delay """
        # Argument e is the event which is created by animation_speed_scale (not used but necessary)
        cfg.ANIMATION_DELAY = int(self.animation_speed_scale.get())

    def generate_maze(self):
        """ Called by generate maze button to validate input and create a maze instance"""        
        self.solve_maze_button.config(state = tk.DISABLED)
        
        try:
            # column validation
            columns = int(self.columns_entry.get())
            if not (cfg.MIN_COLUMNS <= columns <= cfg.MAX_COLUMNS): raise ValueError
            
            try:
                # row validation
                rows = int(self.rows_entry.get())
                if not (cfg.MIN_ROWS <= rows <= cfg.MAX_ROWS): raise ValueError

                Maze.create(self.parent, columns, rows, cfg.PADDING, cfg.CELL_WIDTH, self.show_grid.get())
            except ValueError:
                # row exception
                tk.messagebox.showwarning("Format Error: Height", "Only numbers between " + str(cfg.MIN_ROWS) + " and " + str(cfg.MAX_ROWS) + " allowed!")
        except ValueError:
            # column exception
            tk.messagebox.showwarning("Format Error: Width", "Only numbers between " + str(cfg.MIN_COLUMNS) + " and " + str(cfg.MAX_COLUMNS) + " allowed!")

    def solve_maze(self):
        """ Called on solve maze button click. Disables Button and calls maze solve path """
        self.solve_maze_button.config(state = tk.DISABLED)
        self.parent.maze.solve_path(self.parent.maze.exit.index)
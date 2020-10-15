import tkinter as tk
import tkinter.messagebox
import random
import config as cfg
from cell   import Cell
from player import Player

class Maze(tk.Canvas):
    """ This is the central class which handles and controls the main game logic """

    def __init__(self, parent, columns, rows, padding, cell_width, show_grid):
        """ Initalizes Maze instance for given arguments and starts generating a maze by calling animate_generation """
        # Required vars for the canvas init
        self.columns    = columns
        self.rows       = rows
        self.width      = self.columns * cfg.CELL_WIDTH + cfg.PADDING * 2
        self.height     = self.rows    * cfg.CELL_WIDTH + cfg.PADDING * 2

        # Initalizes canvas
        tk.Canvas.__init__(self, parent, width = self.width, height = self.height) 

        self.set_grid(self.columns, self.rows)
        self.set_random_start_cell()
        self.set_random_exit_cell()

        self.parent          = parent
        self.stack           = []
        self.solution        = {}
        self.job             = None
        self.current         = self.start
        self.current.visited = True
        self.current_cell    = None
        
        if show_grid: self.draw_grid()
        
        # Shows first cell 
        self.current.show()
        self.stack.append(self.current)

        # Sets current_cell overlay to current cell
        self.current_cell = self.create_rectangle(Cell.get_cell_coords(self.current.x, self.current.y), fill = cfg.COLOR_CURRENT, outline = "")
        self.tag_lower(self.current_cell)
        
        # Genereates random maze
        self.animate_generation()


    @staticmethod
    def create(parent, columns, rows, padding, cell_width, show_grid):
        """ Called by settings_bar.generate_maze to create a new maze instance """
        if isinstance(parent.maze, Maze):
            # Cancels potentially scheduling & destroys old instance
            parent.after_cancel(parent.maze.job)
            parent.maze.destroy()
        # Creates new maze instance
        parent.maze = Maze(parent, columns, rows, padding, cell_width, show_grid)
        parent.maze.pack()
    
    def index(self, x, y):
        """ Returns cell from maze or null for given arguments """
        # Handles edge cases
        if not (x < 0 or y < 0 or x > self.columns-1 or y > self.rows-1):
            return self.grid[x + y * self.columns]

    def set_grid(self, x, y):
        """ Clears grid & creates list of cell instances which represent the maze"""
        self.grid = []
        for j in range(y):
            for i in range(x):
                self.grid.append(Cell(self, i, j))

    def draw_grid(self):
        """ Draws cells in grid to canvas"""
        for cell in self.grid: 
            cell.show()

    def set_random_start_cell(self):
        """ Sets random cell from first row as start """
        self.start = self.grid[random.randrange(self.columns)]
    
    def set_random_exit_cell(self):
        """ Sets random cell from last row as exit """
        grid_length = len(self.grid)
        self.exit = self.grid[random.randrange(grid_length - self.columns, grid_length)]

    def animate_generation(self):
        """ Implementation of the recursice backtracking algorithm with visulization"""
        if len(self.stack) > 0:
            next = self.current.get_random_unvisited_neighbor()
            if isinstance(next, Cell):
                self.solution[(next.index)] = self.current.index
                self.stack.append(next)
                self.current.remove_wall(next)
                self.current = next
                self.current.visited = True
                self.current.show()
            else:
                self.current = self.stack.pop()

            # Moves current_cell overlay to new location
            self.coords(self.current_cell, Cell.get_cell_coords(self.current.x, self.current.y))
            self.job = self.parent.after(cfg.ANIMATION_DELAY, self.animate_generation)
        else:
            # Cancels scheduling & removes current cell visulization
            self.parent.after_cancel(self.job)
            self.delete(self.current_cell)
            self.prepare_game()
        
    def prepare_game(self):
        """ Executes after Maze generation, prepares & creates Player to walk maze """
        # Hides visited filling from generation
        for cell in self.grid:
            self.itemconfig(cell.filling, state = "hidden")
        
        # Creates visual entry & exit
        self.delete(self.start.walls[cfg.TOP_WALL], self.exit.walls[cfg.BOTTOM_WALL])

        # Creates instance of Player to walk the maze
        self.player = Player(self, self.start.x, self.start.y)
        self.parent.parent.bind("<Key>", self.player.walk_maze)
        self.parent.settings_bar.solve_maze_button.config(state = "normal")
    
    
    def solve_path(self, i):
        """ Called on solve maze button click. Draws path from cell with index = i to start. """
        if i is not self.start.index:
            self.itemconfig(self.grid[i].filling, fill = cfg.COLOR_SOLVE, state="normal")
            self.tag_lower(self.grid[i].filling)
            i = self.solution[i]
            self.job = self.parent.after(cfg.ANIMATION_DELAY, lambda: self.solve_path(i))
        else:
            self.itemconfig(self.grid[i].filling, fill=cfg.COLOR_SOLVE, state="normal")
            self.tag_lower(self.grid[i].filling)
            self.parent.after_cancel(self.job)
    
    def maze_solved(self):
        """ Handles event for solving the maze. Unbinds key input to supress further player movment """
        self.parent.parent.unbind("<Key>")
        tk.messagebox.showinfo("Maze solved", "Congratulations, you escaped from the maze!")
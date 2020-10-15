import config as cfg
from cell import Cell

class Player:
    """ This class is used to walk the maze """

    def __init__(self, parent, x, y):
        """ Initializes Player instance at given position (x,y)"""
        self.parent = parent
        self.x = x
        self.y = y
        self.filling = self.parent.create_rectangle(Cell.get_cell_coords(self.x, self.y), fill = cfg.COLOR_PLAYER, outline = "")
        self.parent.tag_lower(self.filling)
    

    def walk_maze(self, event):
        """ Called, after maze.prepare_game and handles players movement """
        walls = self.parent.index(self.x, self.y).walls

        if   (event.char == "w" or event.keysym == 'Up'   ) and not walls[cfg.TOP_WALL]   : self.y -= 1
        elif (event.char == "a" or event.keysym == 'Left' ) and not walls[cfg.LEFT_WALL]  : self.x -= 1
        elif (event.char == "s" or event.keysym == 'Down' ) and not walls[cfg.BOTTOM_WALL]: self.y += 1
        elif (event.char == "d" or event.keysym == 'Right') and not walls[cfg.RIGHT_WALL] : self.x += 1

        self.parent.coords(self.filling, Cell.get_cell_coords(self.x, self.y))

        # checks if player found exit
        if (self.x, self.y) == (self.parent.exit.x, self.parent.exit.y):
            self.parent.maze_solved()
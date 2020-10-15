import random
import config as cfg

class Cell:
    """ Maze consists of multiple Cell instances """

    def __init__(self, parent, x, y):
        """ Creates cell instance with the given arguments. By default all walls are set, no filling, not visited"""
        self.parent = parent
        self.x = x
        self.y = y
        self.index = self.x + self.y * self.parent.columns
        self.walls = [True]*4
        self.filling = None
        self.visited = False
    
    
    def get_random_unvisited_neighbor(self):
        """ Returns random unvisted neighbor or null """
        neighbors = []

        top    = self.parent.index(self.x, self.y-1)
        right  = self.parent.index(self.x+1, self.y)
        bottom = self.parent.index(self.x, self.y+1)
        left   = self.parent.index(self.x-1, self.y)

        if top    and not top.visited   : neighbors.append(top)
        if right  and not right.visited : neighbors.append(right)
        if bottom and not bottom.visited: neighbors.append(bottom)
        if left   and not left.visited  : neighbors.append(left)

        if len(neighbors) > 0: 
            return neighbors[random.randrange(len(neighbors))]
    
    def remove_wall(self, b):
        """ Removes wall between self and cell b """
        x = self.x - b.x
        y = self.y - b.y

        # rm_index = Tupel(delete_wall_a_index, delete_wall_b_index)
        if   x ==  1 and y ==  0: rm_index = cfg.LEFT_WALL  , cfg.RIGHT_WALL
        elif x == -1 and y ==  0: rm_index = cfg.RIGHT_WALL , cfg.LEFT_WALL
        elif x ==  0 and y ==  1: rm_index = cfg.TOP_WALL   , cfg.BOTTOM_WALL
        elif x ==  0 and y == -1: rm_index = cfg.BOTTOM_WALL, cfg.TOP_WALL

        self.parent.delete(self.walls[rm_index[0]], b.walls[rm_index[1]])
        self.walls[rm_index[0]] = False
        b.walls[rm_index[1]]    = False
    
    def show(self):
        """ Draws instance on parents canvas """
        # required coords to create walls
        xs_pos = self.x * cfg.CELL_WIDTH + cfg.PADDING
        ys_pos = self.y * cfg.CELL_WIDTH + cfg.PADDING
        xl_pos = xs_pos + cfg.CELL_WIDTH
        yl_pos = ys_pos + cfg.CELL_WIDTH
            
        if self.walls[cfg.TOP_WALL]    is True: self.walls[cfg.TOP_WALL]    = self.parent.create_line(xs_pos, ys_pos, xl_pos, ys_pos)
        if self.walls[cfg.RIGHT_WALL]  is True: self.walls[cfg.RIGHT_WALL]  = self.parent.create_line(xl_pos, ys_pos, xl_pos, yl_pos)
        if self.walls[cfg.BOTTOM_WALL] is True: self.walls[cfg.BOTTOM_WALL] = self.parent.create_line(xl_pos, yl_pos, xs_pos, yl_pos)
        if self.walls[cfg.LEFT_WALL]   is True: self.walls[cfg.LEFT_WALL]   = self.parent.create_line(xs_pos, yl_pos, xs_pos, ys_pos)

        if self.visited and not self.filling:
            self.filling = self.parent.create_rectangle(xs_pos, ys_pos, xl_pos, yl_pos , fill = cfg.COLOR_VISITED, outline = "")
            self.parent.tag_lower(self.filling)
    
    @staticmethod
    def get_cell_coords(x, y):
        """ helper function to get top-left & bottom-right coords for given arguments """
        x = x * cfg.CELL_WIDTH + cfg.PADDING
        y = y * cfg.CELL_WIDTH + cfg.PADDING
        return (x, y, x + cfg.CELL_WIDTH, y + cfg.CELL_WIDTH)
import copy
from dlgo.gotypes import Point

class Move():
    # Any action will be set to either play, pass, or resign
    def __init__(self, point=None, is_pass=False, is_resign=False):
        assert (point is not None) ^ is_pass ^ is_resign
        self.point = point
        self.is_play = (self.point is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign

    @classmethod
    def play(cls, point):
        return Move(point=point)
    
    @classmethod
    def play(cls, point):
        return Move(point=point)
    
    @classmethod
    def pass_turn(cls):
        return Move(is_pass=True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign=True)



class GoString():
    # Class to represent a string of stones using a set
    def __init__(self, color, stones: list[Point], liberties):
        self.color=color
        self.stones = set(stones)
        self.liberties = set(liberties)
    
    def remove_liberty(self, point):
        self.liberties.remove(point)

    def add_liberty(self, point):
        self.liberties.add(point)

    def merged_with(self, go_string: 'GoString'):
        '''
        Called when a player connects two of its groups by placing a stone.
        Returns a new GoString containing all the stones in both strings.
        '''
        assert go_string.color == self.color
        combined_stones = self.stones | go_string.stones
        return GoString(self.color, combined_stones, (self.liberties | go_string.liberties) - combined_stones)
    
    @property
    def num_liberties(self):
        '''
        Allowing the strings to track their own liberties means that we do not have to
        count the liberties of each stone individually, which will get increasingly complex
        and inefficient with the length of each string/amount of stones on the board in general
        '''
        return len(self.liberties)
    
    def __eq__(self, other):
        return isinstance(other, GoString) \
        and self.color == other.color \
        and self.stones == other.stones \
        and self.liberties == other.liberties



class Board():
    def __init__(self, num_rows, num_cols):
        # Creates the Board
        self.num_rows = num_rows
        self.num_cols = num_cols
        self._grid = {} 

    def place_stone(self, player, point: Point):
        '''
        1. Check if the point exists, and is not occupied
        2. Identify point liberties, adjacent same colors, adjacent opposite colours
        4. Merge with adjacent same colour strings
        5. Reduce liberties for adjacent opposite colours
        6. Remove any strings with 0 liberties
        '''
        assert self.is_on_grid(point)
        assert self._grid.get(point) is None

        adjacent_same_color: list[GoString] = []
        adjacent_opposite_color: list[GoString] = []
        liberties = []

        for neighbour in point.neighbours():
            if not self.is_on_grid(neighbour):
                continue

            neighbour_string = self._grid.get(neighbour)
            if neighbour_string is None:
                liberties.append(neighbour)
            elif neighbour_string.color == player:
                if neighbour_string not in adjacent_same_color: adjacent_same_color.append(neighbour_string)
                else:
                    if neighbour_string not in adjacent_opposite_color: adjacent_opposite_color.append(neighbour_string)
            
        new_string = GoString(player, [point], liberties)

        for same_color_string in adjacent_same_color:
            new_string = new_string.merged_with(same_color_string)
            for new_string_point in new_string.stones:
                self._grid[new_string_point] = new_string
        
        for other_color_string in adjacent_opposite_color:
            other_color_string.remove_liberty(point)
        for other_color_string in adjacent_opposite_color:
            if other_color_string.num_liberties == 0:
                self._remove_string(other_color_string)

    def is_on_grid(self, point: 'Point'):
        return 1 <= point.row <= self.num_rows \
        and 1 <= point.col <= self.num_cols
    
    def get(self, point: 'Point'):
        # Return the content of a point on the board --> Player if there is a stone, otherwise None
        string = self._grid.get(point)
        if string is None:
            return None
        return string.color
    
    def get_go_string(self, point: 'Point'):
        # Returns the entire string of stones at a point --> GoString if there is a stone, otherwise None
        string = self._grid.get(point)
        if string is None:
            return None
        return string
    
    def _remove_string(self, string: GoString):
        '''
        Removing a string can create liberties for other strings. As such, we will loop through each point
        in the string, find that point's neighbours, and re-add the point as a liberty. Then, we will set
        the point itself to be empty.
        '''
        for point in string.stones:
            for neighbour in point.neighbours():
                neighbour_string = self._grid.get(neighbour)
                if neighbour_string is None: continue
                if neighbour_string is not string: neighbour_string.add_liberty(point)
            self._grid[point] = None
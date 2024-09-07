from dlgo.gotypes import Point
from dlgo.goboard_slow import Board

def is_point_an_eye(board: Board, point: Point, color):
    '''
    1. Check if point is empty --> an eye is an empty point
    2. Check if all adjacent points contain friendly stones
    3. Three of Four corners must be controlled. If on the edge, ALL corners must be controlled
        A. If point is edge/corner --> check that all corners are controlled
        B. If point is inside the board --> check that at least 3 corners are controlled
    '''
    if board.get(point) is not None:
        return False
    for neighbour in point.neighbours():
        if board.is_on_grid(neighbour):
            neighbour_color = board.get(neighbour)
            if neighbour_color != color:
                return False
    
    friendly_corners = 0
    off_board_corners = 0
    corners = [
        Point(point.row - 1, point.col - 1),
        Point(point.row - 1, point.col + 1),
        Point(point.row + 1, point.col - 1),
        Point(point.row + 1, point.col + 1),
    ]
    for corner in corners:
        if board.is_on_grid(corner):
            corner_color = board.get(corner)
            if corner_color == color: 
                friendly_corners += 1
        else: 
            off_board_corners += 1
    if off_board_corners > 0:
        return off_board_corners + friendly_corners == 4
    return friendly_corners >= 3            
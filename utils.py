import math

BOARD_SIZE = 50
NEGATIVE_INF = -math.inf
INF = math.inf

class RenderingPos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def to_board_pos(self, board_offset):
        return BoardPos(
            math.floor((self.y - board_offset.y) / BOARD_SIZE),
            math.floor((self.x - board_offset.x) / BOARD_SIZE)
        )

class BoardPos:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    
    def to_rendering_pos(self, board_offset):
        return RenderingPos(
            (self.col * BOARD_SIZE) + board_offset.x,
            (self.row * BOARD_SIZE) + board_offset.y
        )
    
    def on_board(self):
        return 0 <= self.row <= 7 and 0 <= self.col <= 7
    
    def get_square(self, board):
        return board.squares[self.row][self.col]

    def equals(self, board_pos):
        return self.row == board_pos.row and self.col == board_pos.col

class Move:
    def __init__(self, start, dest):
        self.start = start
        self.dest = dest
    
    def to_str(self):
        return f"{self.start.row}, {self.start.col} -> {self.dest.row}, {self.dest.col}"

class BoardValueMap:
    def __init__(self, values, is_white):
        self.values = values
        if not is_white:
            self.values.reverse()

    
    def get_value(self, board_pos):
        return self.values[board_pos.row][board_pos.col]
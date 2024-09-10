import pygame as pg
from utils import RenderingPos, BoardPos, Move, BoardValueMap, BOARD_SIZE

class Piece:
    def __init__(self, pos, is_white):
        self.is_white = is_white
        self.pos = pos
        self.value = 0

        self.board_value_map = BoardValueMap(
            [[0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]],
            is_white
        )
        
        color = "white" if self.is_white else "black"
        piece_name = type(self).__name__
        if piece_name != "EmptyPiece":
            self.sprite = pg.transform.scale(
                pg.image.load(f"engine2\sprites\\{color}_{piece_name}.png"),
                (BOARD_SIZE, BOARD_SIZE)
            )
        else:
            self.sprite = None
    
    def draw(self, WIN, pos):
        if self.sprite != None:
            WIN.blit(self.sprite, pos)
    
    def generate_moves_no_check(self, board):
        return []
    
    def generate_legal_moves(self, board):
        moves = []

        for move in self.generate_moves_no_check(board):
            test_position = board.test(move)

            legal = True
            for response_move in test_position.generate_moves_no_check():
                target = response_move.dest.get_square(test_position)
                if type(target) == King and target.is_white == board.white_turn:
                    legal = False
            
            if legal:
                moves.append(move)
        
        return moves

    def is_empty(self):
        return False
    
    def get_value(self):
        return self.value + self.board_value_map.get_value(self.pos)

class EmptyPiece(Piece):
    def __init__(self, pos):
        super().__init__(pos, None)
        self.__name__ = None
    
    def is_empty(self):
        return True

class Pawn(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.value = 1

        '''
        self.board_value_map = BoardValueMap(
            [[0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5],
            [0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2],
            [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1],
            [0,0,0.5,0.5,0.5,0.5,0,0],
            [0,0,0.5,1,1,0.5,0,0],
            [0,0,0.3,0.5,0.5,0.3,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]],
            is_white
        )'''
    
    def generate_moves_no_check(self, board):
        moves = []

        if self.is_white != board.white_turn:
            return moves

        turn_multiplier = 1
        if self.is_white:
            turn_multiplier = -1
        
        one_step_target = board.squares[self.pos.row + turn_multiplier][self.pos.col]
        if one_step_target.is_empty():
            moves.append(
                Move(self.pos, BoardPos(self.pos.row + turn_multiplier, self.pos.col))
            )
        
            two_step_target = board.squares[self.pos.row + (2 * turn_multiplier)][self.pos.col]
            if ((self.pos.row == 6 and self.is_white) or (self.pos.row == 1 and not self.is_white)) and two_step_target.is_empty():
                moves.append(
                    Move(self.pos, BoardPos(self.pos.row + (2 * turn_multiplier), self.pos.col))
                )
        
        left_dia_pos = BoardPos(self.pos.row + turn_multiplier, self.pos.col - 1)
        if left_dia_pos.on_board() and left_dia_pos.get_square(board).is_white != self.is_white and not left_dia_pos.get_square(board).is_empty():
            moves.append(
                Move(self.pos, left_dia_pos)
            )
        
        right_dia_pos = BoardPos(self.pos.row + turn_multiplier, self.pos.col + 1)
        if right_dia_pos.on_board() and right_dia_pos.get_square(board).is_white != self.is_white and not right_dia_pos.get_square(board).is_empty():
            moves.append(
                Move(self.pos, right_dia_pos)
            )

        return moves

class Bishop(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.value = 3

    def generate_moves_no_check(self, board):
        moves = []

        if self.is_white != board.white_turn:
            return moves
        
        for dRow, dCol in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            multiplier = 1
            target_pos = BoardPos(self.pos.row + dRow, self.pos.col + dCol)
            while target_pos.on_board() and target_pos.get_square(board).is_white != self.is_white:
                moves.append(
                    Move(self.pos, target_pos)
                )

                if target_pos.get_square(board).is_white != None:
                    break

                multiplier += 1
                target_pos = BoardPos(self.pos.row + (multiplier * dRow), self.pos.col + (multiplier * dCol))
        
        return moves
    
class Rook(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.value = 5
    
    def generate_moves_no_check(self, board):
        moves = []

        if self.is_white != board.white_turn:
            return moves
        
        for dRow, dCol in [(-1, -0), (1, 0), (0, -1), (0, 1)]:
            multiplier = 1
            target_pos = BoardPos(self.pos.row + dRow, self.pos.col + dCol)
            while target_pos.on_board() and target_pos.get_square(board).is_white != self.is_white:
                moves.append(
                    Move(self.pos, target_pos)
                )

                if target_pos.get_square(board).is_white != None:
                    break

                multiplier += 1
                target_pos = BoardPos(self.pos.row + (multiplier * dRow), self.pos.col + (multiplier * dCol))
        
        return moves

class Queen(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.value = 9

    def generate_moves_no_check(self, board):
        moves = []

        if self.is_white != board.white_turn:
            return moves
        
        for dRow in range(-1, 2):
            for dCol in range(-1, 2):
                multiplier = 1
                target_pos = BoardPos(self.pos.row + dRow, self.pos.col + dCol)
                while target_pos.on_board() and target_pos.get_square(board).is_white != self.is_white:
                    moves.append(
                        Move(self.pos, target_pos)
                    )

                    if target_pos.get_square(board).is_white != None:
                        break

                    multiplier += 1
                    target_pos = BoardPos(self.pos.row + (multiplier * dRow), self.pos.col + (multiplier * dCol))

        return moves

class Knight(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.value = 3
    
    def generate_moves_no_check(self, board):
        moves = []

        if self.is_white != board.white_turn:
            return moves
        
        for dRow in [-2, 2]:
            for dCol in [-1, 1]:
                target_pos = BoardPos(self.pos.row + dRow, self.pos.col + dCol)
                if target_pos.on_board() and target_pos.get_square(board).is_white != self.is_white:
                    moves.append(
                        Move(self.pos, target_pos)
                    )
        
        for dRow in [-1, 1]:
            for dCol in [-2, 2]:
                target_pos = BoardPos(self.pos.row + dRow, self.pos.col + dCol)
                if target_pos.on_board() and target_pos.get_square(board).is_white != self.is_white:
                    moves.append(
                        Move(self.pos, target_pos)
                    )
        
        return moves

class King(Piece):
    def __init__(self, pos, is_white):
        super().__init__(pos, is_white)
        self.value = 1000
    
    def generate_moves_no_check(self, board):
        moves = []

        if self.is_white != board.white_turn:
            return moves
        
        for dRow in range(-1, 2):
            for dCol in range(-1, 2):

                target_pos = BoardPos(self.pos.row + dRow, self.pos.col + dCol)
                if target_pos.on_board() and target_pos.get_square(board).is_white != self.is_white:
                    moves.append(
                        Move(self.pos, target_pos)
                    )
        
        return moves

class Board:
    FEN_DECODE = {
        'p' : Pawn,
        'P' : Pawn,
        'b' : Bishop,
        'B' : Bishop,
        'n' : Knight,
        'N' : Knight,
        'r' : Rook,
        'R' : Rook,
        'q' : Queen,
        'Q' : Queen,
        'k' : King,
        'K' : King
    }

    def __init__(self, initial):
        if type(initial) == str:
            self.squares = self.fen_to_squares(initial)
        elif type(initial) == list:
            self.squares = initial

        self.white_turn = True

        self.piece_squares = []
        for row in self.squares:
            for piece in row:
                if type(piece) != EmptyPiece:
                    self.piece_squares.append(piece)
    
    def fen_to_squares(self, fen):
        squares = []

        fen_rows = fen.split('/')

        for row_i, fen_row in enumerate(fen_rows):
            row = []
            col_i = 0
            for piece in fen_row:
                if piece.isnumeric():
                    for i in range(int(piece)):
                        col_i += 1
                        row.append(EmptyPiece(BoardPos(row_i, col_i)))
                else:
                    row.append(self.FEN_DECODE[piece](BoardPos(row_i, col_i), piece.isupper()))
                    col_i += 1
            squares.append(row)
        
        return squares

    def generate_moves_no_check(self):
        moves = []

        for piece in self.piece_squares:
            if piece.is_white == self.white_turn:
                moves += piece.generate_moves_no_check(self)
        
        return moves

    def generate_legal_moves(self):
        moves = []

        for piece in self.piece_squares:
            moves += piece.generate_legal_moves(self)
        
        return moves

    def make(self, move):

        if not self.squares[move.dest.row][move.dest.col].is_empty():
            self.piece_squares.remove(self.squares[move.dest.row][move.dest.col])

        self.squares[move.dest.row][move.dest.col] = self.squares[move.start.row][move.start.col]
        if (move.dest.row == 0 or move.dest.row == 7) and type(self.squares[move.dest.row][move.dest.col]) == Pawn:
            self.piece_squares.remove(self.squares[move.dest.row][move.dest.col])
            new_queen = Queen(move.dest, self.squares[move.dest.row][move.dest.col].is_white)
            self.squares[move.dest.row][move.dest.col] = new_queen
            self.piece_squares.append(new_queen)
        self.squares[move.dest.row][move.dest.col].pos = move.dest
        self.squares[move.start.row][move.start.col] = EmptyPiece(move.start)

        self.white_turn = not self.white_turn

    def test(self, move):
        squares = []

        for row in self.squares:
            n_row = []
            for square in row:
                if type(square) == EmptyPiece:
                    n_row.append(type(square)(square.pos))
                else:
                    n_row.append(type(square)(square.pos, square.is_white))
            squares.append(n_row)
        
        n_board = Board(squares)
        n_board.white_turn = self.white_turn
        n_board.make(move)

        return n_board

class Rendering_Board:
    def __init__(self, board, board_pos=RenderingPos(0, 0), dark_color=(0, 0, 0), light_color=(255, 255, 255)):
        self.board = board

        #rendering info
        self.rendering_pos = board_pos
        self.DARK_SQUARE = dark_color
        self.LIGHT_SQUARE = light_color

        self.current_selection = EmptyPiece(BoardPos(3, 4))
        self.reachable_positions = [move.dest for move in self.board.generate_legal_moves()]
    
    def update(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()
            mouse_board_pos = RenderingPos(mouse_x, mouse_y).to_board_pos(self.rendering_pos)
            if mouse_board_pos.on_board() and mouse_board_pos.get_square(self.board).is_white == self.board.white_turn:
                self.current_selection = self.board.squares[mouse_board_pos.row][mouse_board_pos.col]
            elif mouse_board_pos.on_board() and self.current_selection.is_white == self.board.white_turn:
                legal = False
                for move in self.current_selection.generate_legal_moves(self.board):
                    if move.start.equals(self.current_selection.pos) and move.dest.equals(mouse_board_pos):
                        legal = True
                
                if legal:
                    self.board.make(Move(self.current_selection.pos, mouse_board_pos))
                    self.reachable_positions = [move.dest for move in self.board.generate_legal_moves()]

    def draw(self, WIN):
        
        for row, board_row in enumerate(self.board.squares):
            for col, square in enumerate(board_row):
                pg.draw.rect(WIN, self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE, 
                             pg.Rect((col * BOARD_SIZE) + self.rendering_pos.x, 
                                     (row * BOARD_SIZE) + self.rendering_pos.y,
                                     BOARD_SIZE,
                                     BOARD_SIZE))
                
                if square != None:
                    square.draw(WIN, 
                                ((col * BOARD_SIZE) + self.rendering_pos.x, 
                                (row * BOARD_SIZE) + self.rendering_pos.y))
        
        self.draw_potential_moves(WIN)
    
    def draw_potential_moves(self, WIN):

        for dest in self.reachable_positions:
            rendering_dest = dest.to_rendering_pos(self.rendering_pos)
            pg.draw.circle(WIN, (196, 188, 188), 
                           (rendering_dest.x + (BOARD_SIZE / 2),
                            rendering_dest.y + (BOARD_SIZE / 2)),
                            BOARD_SIZE / 4)

        if self.current_selection != None:
            potential_moves = self.current_selection.generate_legal_moves(self.board)

            for move in potential_moves:
                rendering_dest = move.dest.to_rendering_pos(self.rendering_pos)
                pg.draw.circle(WIN, (100, 0, 0), 
                               (rendering_dest.x + (BOARD_SIZE / 2),
                                rendering_dest.y + (BOARD_SIZE / 2)),
                                BOARD_SIZE / 4)
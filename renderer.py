import pygame as pg
import sys
from pieces import Board, Rendering_Board
from utils import RenderingPos
from engine import Engine

pg.init()

WIDTH, HEIGHT = 600, 600
WIN = pg.display.set_mode((WIDTH, HEIGHT))

DARK_SQUARE = (111,143,114)
LIGHT_SQUARE = (173,189,143)
BACKGROUND = (29, 94, 76)

board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
#board = Board("8/pp6/8/3n4/3PP3/8/8/2B5")
rendering_board = Rendering_Board(board, 
              board_pos=RenderingPos(100, 100),
              dark_color= DARK_SQUARE,
              light_color= LIGHT_SQUARE)
engine = Engine()

running = True
while running:
    events = pg.event.get()
    for event in events:
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                #print("EVAL COMPARISON")
                #print(engine.depth_1_best_move(board).eval)
                #print(engine.depth_best_move(board, 1))

                engine.best_move_search(board, 1)
        
        rendering_board.update(event)
    
    WIN.fill(BACKGROUND)
    rendering_board.draw(WIN)

    pg.display.update()
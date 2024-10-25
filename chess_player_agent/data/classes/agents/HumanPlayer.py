# /* HumanAgent.py

import pygame
import typing

from data.classes.Square import Square
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent

class HumanPlayer(ChessAgent):

    def choose_action(self, board: Board):
        assert(board.turn == self.color)
        choosing_move = True
        while choosing_move:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    move = self.handle_click(board, *pygame.mouse.get_pos())
                    if move is not None:
                        return move
            board.draw()

    def handle_click(self, board: Board, mx: float, my: float) \
                     -> tuple[Square, Square]:
        x = mx // board.tile_width
        y = my // board.tile_height
        clicked_square = board.get_square_from_pos((x, y))
        if clicked_square.occupying_piece is not None \
            and clicked_square.occupying_piece.color == board.turn:
            board.select_square(clicked_square)
        elif board.selected_square is not None \
             and clicked_square in \
                 board.selected_square.occupying_piece.get_valid_moves(board):
            return (board.selected_square, clicked_square)
        else:
            board.select_square(None)
        return None
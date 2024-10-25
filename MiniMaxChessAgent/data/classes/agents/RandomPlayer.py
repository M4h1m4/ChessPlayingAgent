# /* RandomAgent.py

import random

from data.classes.Square import Square
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent

class RandomPlayer(ChessAgent):
    def choose_action(self, board: Board):
        possible_moves: list[tuple[Square, Square]] = []
        for square in board.squares:
            if square.occupying_piece != None \
               and square.occupying_piece.color == self.color:
                for target in square.occupying_piece.get_valid_moves(board):
                    possible_moves.append((square, target))
        if len(possible_moves) < 1:
            return False
        return random.choice(possible_moves)

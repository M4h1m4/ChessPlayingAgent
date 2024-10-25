# /* Piece.py

from __future__ import annotations
import pygame

from typing import Literal, TYPE_CHECKING
if TYPE_CHECKING:
    from data.classes.Board import Board
    from data.classes.Square import Square

class Piece:
    def __init__(self, pos: tuple[int, int], color: Literal['white', 'black'],
                 board: Board):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.notation = ' '
        self.has_moved: bool = False
        self.img: pygame.surface.Surface = None

    def get_possible_moves(self) -> list[list[Square]]:
        # Must be implemented by child classes
        assert(False)

    def get_moves(self, board: Board) -> list[Square]:
        output: list[Square] = []
        for direction in self.get_possible_moves(board):
            direction: list[Square]
            for square in direction:
                square: Square
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        output.append(square)
                        break
                else:
                    output.append(square)
        return output

    def get_valid_moves(self, board: Board) -> list[Square]:
        output: list[Square] = []
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                output.append(square)
        return output

    def move(self, board: Board, square: Square, force: bool=False) -> bool:
        if (square is None):
            return False
        for i in board.squares:
            i.highlight = False
        if square in self.get_valid_moves(board) or force:
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_square = None
            self.has_moved = True
            # Pawn promotion
            if self.notation == ' ':
                if self.y == 0 or self.y == 7:
                    from data.classes.pieces.Queen import Queen
                    square.occupying_piece = Queen(
                        (self.x, self.y),
                        self.color,
                        board
                    )
            # Move rook if king castles
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
            return True
        else:
            board.selected_square = None
            return False

    # True for all pieces except pawn
    def attacking_squares(self, board: Board) -> bool:
        return self.get_moves(board)
# /* Board.py

import pygame

from typing import Literal
from data.classes.Square import Square
from data.classes.Piece import Piece
from data.classes.pieces.Rook import Rook
from data.classes.pieces.Bishop import Bishop
from data.classes.pieces.Knight import Knight
from data.classes.pieces.Queen import Queen
from data.classes.pieces.King import King
from data.classes.pieces.Pawn import Pawn

# Game state checker
class Board:
    def __init__(self, display: pygame.surface.Surface, width: float, height: float):
        self.display = display
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_square: Square = None
        self.turn: Literal['white', 'black'] = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.squares: list[Square] = self.generate_squares()
        self.setup_board()

    def generate_squares(self) -> list[Square]:
        output: list[Square] = []
        for y in range(8):
            for x in range(8):
                output.append(
                    Square(x,  y, self.tile_width, self.tile_height)
                )
        return output

    def get_square_from_pos(self, pos: tuple[float, float]) -> Square:
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos: tuple[float, float]) -> Piece:
        return self.get_square_from_pos(pos).occupying_piece

    def select_square(self, square: Square):
        for s in self.squares:
            s.highlight = False
        self.selected_square = square

    def setup_board(self) -> None:
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))
                    # looking inside contents, what piece does it have
                    if piece[1] == 'R':
                        square.occupying_piece = Rook(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    # as you notice above, we put `self` as argument, or means our class Board
                    elif piece[1] == 'N':
                        square.occupying_piece = Knight(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'B':
                        square.occupying_piece = Bishop(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'Q':
                        square.occupying_piece = Queen(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'K':
                        square.occupying_piece = King(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    elif piece[1] == 'P':
                        square.occupying_piece = Pawn(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )

    def handle_move(self, from_square: Square, to_square: Square) -> bool:
        if from_square.occupying_piece is not None:
            if from_square.occupying_piece.move(self, to_square):
                self.turn = 'white' if self.turn == 'black' else 'black'
                return True
        
        return False

    # check state checker
    def is_in_check(self, color: Literal['white', 'black'],
                    board_change: tuple[tuple[int, int],
                                        tuple[int, int]]=None) -> bool:
        # board_change = [(x1, y1), (x2, y2)]
        output = False
        king_pos: tuple[int, int] = None
        changing_piece: Piece = None
        old_square: Square = None
        new_square: Square = None
        new_square_old_piece: Piece = None
        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        pieces = [
            i.occupying_piece for i in self.squares if i.occupying_piece is not None
        ]
        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
        if king_pos == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                        king_pos = piece.pos
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        output = True
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        return output

    # checkmate state checker
    def is_in_checkmate(self, color: Literal['white', 'black']):
        if not self.is_in_check(color):
            return False
        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None and piece.color == color \
                and len(piece.get_valid_moves(self)) > 0:
                return False
        return True

    def draw(self, display: pygame.surface.Surface = None):
        if display == None:
            display = self.display
        display.fill('white')
        if self.selected_square is not None:
            self.selected_square.highlight = True
            for square in self.selected_square.occupying_piece.get_valid_moves(self):
                square.highlight = True
        for square in self.squares:
            square.draw(display)
        pygame.display.update()
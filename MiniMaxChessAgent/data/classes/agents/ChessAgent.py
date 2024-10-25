# /* ChessAgent.py

from typing import Literal
from data.classes.Square import Square
from data.classes.Board import Board

class ChessAgent:
    # Create private variables for Agent
    def __init__(self, color: Literal['white', 'black']):
        # In child classes, feel free to initialize any other state
        # or helper fuctions
        self.color = color

    def choose_action(self, board: Board) -> tuple[Square, Square] | bool:
        return False
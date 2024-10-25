from typing import Literal, List, Tuple
from data.classes.Board import Board

class SmSq:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.occupying_piece: SimulationPiece = None

class SimulationPiece:
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        self.pos = pos
        self.color = color
        self.notation = ' '
        self.has_moved = False

    def get_valid_moves(self, board: 'SimulationBoard') -> List[SmSq]:
        # To be implemented in specific piece subclasses
        return []

class SimulationPawn(SimulationPiece):
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        super().__init__(pos, color)
        self.notation = 'P'

    def get_valid_moves(self, board: 'SimulationBoard') -> List['SmSq']:
        valid_moves = []

        # Determine movement direction based on the pawn's color
        direction = -1 if self.color == 'white' else 1

        # Get the current position of the pawn
        curr_x, curr_y = self.pos

        # Normal pawn movement (forward by 1 square)
        forward_pos = (curr_x, curr_y + direction)

        # Check if the forward square is empty
        if board.is_empty(forward_pos):
            valid_moves.append(forward_pos)

        # Pawn capturing logic (diagonal moves)
        for diag_x in [-1, 1]:  # Diagonals (left and right)
            diagonal_pos = (curr_x + diag_x, curr_y + direction)
            if board.is_enemy(diagonal_pos, self.color):  # Can capture if there's an enemy piece
                valid_moves.append(diagonal_pos)

        return valid_moves

class SimulationKnight(SimulationPiece):
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        super().__init__(pos, color)
        self.notation = 'N'


    def get_valid_moves(self, board: 'SimulationBoard') -> List['SmSq']:
        valid_moves = []
        x, y = self.pos
        
        # Knight moves (L-shape)
        moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]

        for dx, dy in moves:
            target_x = x + dx
            target_y = y + dy
            
            if 0 <= target_x < 8 and 0 <= target_y < 8:
                target_square = board.get_square((target_x, target_y))
                if target_square.occupying_piece is None or target_square.occupying_piece.color != self.color:
                    valid_moves.append(target_square)  # Move or capture

        return valid_moves

class SimulationRook(SimulationPiece):
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        super().__init__(pos, color)
        self.notation = 'R'

    def get_valid_moves(self, board: 'SimulationBoard') -> List['SmSq']:
        valid_moves = []
        x, y = self.pos

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up
        
        for dx, dy in directions:
            for i in range(1, 8):
                target_x = x + dx * i
                target_y = y + dy * i
                
                if 0 <= target_x < 8 and 0 <= target_y < 8:
                    target_square = board.get_square((target_x, target_y))
                    if target_square.occupying_piece is None:
                        valid_moves.append(target_square)  # Empty square
                    elif target_square.occupying_piece.color != self.color:
                        valid_moves.append(target_square)  # Capture
                        break
                    else:
                        break  # Blocked by own piece
                else:
                    break  # Out of bounds

        return valid_moves

class SimulationBishop(SimulationPiece):
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        super().__init__(pos, color)
        self.notation = 'B'

    def get_valid_moves(self, board: 'SimulationBoard') -> List['SmSq']:
        valid_moves = []
        x, y = self.pos

        # Diagonal moves
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]  # Down-Right, Up-Right, Down-Left, Up-Left
        
        for dx, dy in directions:
            for i in range(1, 8):
                target_x = x + dx * i
                target_y = y + dy * i
                
                if 0 <= target_x < 8 and 0 <= target_y < 8:
                    target_square = board.get_square((target_x, target_y))
                    if target_square.occupying_piece is None:
                        valid_moves.append(target_square)  # Empty square
                    elif target_square.occupying_piece.color != self.color:
                        valid_moves.append(target_square)  # Capture
                        break
                    else:
                        break  # Blocked by own piece
                else:
                    break  # Out of bounds

        return valid_moves

class SimulationQueen(SimulationPiece):
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        super().__init__(pos, color)
        self.notation = 'Q'

    def get_valid_moves(self, board: 'SimulationBoard') -> List['SmSq']:
        valid_moves = []
        
        # Combine rook and bishop movements
        rook = SimulationRook(self.pos, self.color)
        bishop = SimulationBishop(self.pos, self.color)
        
        valid_moves.extend(rook.get_valid_moves(board))
        valid_moves.extend(bishop.get_valid_moves(board))

        return valid_moves

class SimulationKing(SimulationPiece):
    def __init__(self, pos: Tuple[int, int], color: Literal['white', 'black']):
        super().__init__(pos, color)
        self.notation = 'K'

    def get_valid_moves(self, board: 'SimulationBoard') -> List['SmSq']:
        valid_moves = []
        x, y = self.pos

        # King can move one square in any direction
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            target_x = x + dx
            target_y = y + dy
            
            if 0 <= target_x < 8 and 0 <= target_y < 8:
                target_square = board.get_square((target_x, target_y))
                if target_square.occupying_piece is None or target_square.occupying_piece.color != self.color:
                    valid_moves.append(target_square)  # Move or capture

        return valid_moves

class SimulationBoard:
    def __init__(self):
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
        self.turn: Literal['white', 'black'] = 'white'
        self.squares: List[SmSq] = self.generate_squares()
        self.setup_board()

    def generate_squares(self) -> List[SmSq]:
        output: list[SmSq] = []
        for y in range(8):
            for x in range(8):
                output.append(
                    SmSq(x,  y)
                )
        return output

    def get_square(self, pos) -> SmSq:
        for square in self.squares:
            if (square.x, square.y) == (pos[0],pos[1]):
                return square

    def setup_board(self):
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square((x, y))
                    piece_color = 'white' if piece[0] == 'w' else 'black'
                    piece_notation = piece[1]

                    # Instantiate the appropriate piece class based on notation
                    if piece_notation == 'R':
                        square.occupying_piece = SimulationRook((x, y), piece_color)
                    elif piece_notation == 'N':
                        square.occupying_piece = SimulationKnight((x, y), piece_color)
                    elif piece_notation == 'B':
                        square.occupying_piece = SimulationBishop((x, y), piece_color)
                    elif piece_notation == 'Q':
                        square.occupying_piece = SimulationQueen((x, y), piece_color)
                    elif piece_notation == 'K':
                        square.occupying_piece = SimulationKing((x, y), piece_color)
                    elif piece_notation == 'P':
                        square.occupying_piece = SimulationPawn((x, y), piece_color)
                    
                    square.occupying_piece.color = piece_color


    def handle_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        from_square = self.get_square(from_pos)
        to_square = self.get_square(to_pos)
        if from_square and from_square.occupying_piece:
            piece = from_square.occupying_piece
            if to_square in piece.get_valid_moves(self):
                to_square.occupying_piece = piece
                from_square.occupying_piece = None
                piece.pos = to_pos
                self.turn = 'white' if self.turn == 'black' else 'black'
                return True
        return False

    def is_in_check(self, color: Literal['white', 'black']) -> bool:
        # Simplified check logic
        return False

    def is_in_checkmate(self, color: Literal['white', 'black']) -> bool:
        if not self.is_in_check(color):
            return False
        # Check for no valid moves
        return True

    def copy_from_board(self, board: Board):
        # First, clear any existing squares in the SimulationBoard
        self.squares.clear()

        # Copy basic attributes
        self.turn = board.turn
        self.selected_square = board.selected_square  # This may need deeper copy depending on how you use it

        # Loop through the original board's squares and copy the pieces
        for square in board.squares:
            # simulation_square = SimulationSquare(square.x, square.y, self.tile_width, self.tile_height)
            simulation_square = SmSq(square.x, square.y)
            if square.occupying_piece:
                piece_notation = square.occupying_piece.notation
                piece_color = square.occupying_piece.color
                
                if piece_notation == 'R':
                        simulation_square.occupying_piece = SimulationRook((square.x,square.y), piece_color)
                elif piece_notation == 'N':
                        simulation_square.occupying_piece = SimulationKnight((square.x,square.y), piece_color)
                elif piece_notation == 'B':
                        simulation_square.occupying_piece = SimulationBishop((square.x,square.y), piece_color)
                elif piece_notation == 'Q':
                        simulation_square.occupying_piece = SimulationQueen((square.x,square.y), piece_color)
                elif piece_notation == 'K':
                        simulation_square.occupying_piece = SimulationKing((square.x,square.y), piece_color)
                elif piece_notation == 'P':
                        simulation_square.occupying_piece = SimulationPawn((square.x,square.y), piece_color)
            self.squares.append(simulation_square)

    
    def make_move(self, from_square: SmSq, to_square: SmSq):
        """Make a move from one square to another on the simulation board."""
        # Move the piece from the starting square to the destination square
        if from_square.occupying_piece and to_square not in from_square.occupying_piece.get_valid_moves(self):
            return False  # Invalid move

        # Capture the piece if the destination square has an occupying piece
        if to_square.occupying_piece:
            to_square.occupying_piece = None  # Remove the captured piece

        # Move the piece
        to_square.occupying_piece = from_square.occupying_piece
        from_square.occupying_piece = None  # Clear the starting square

        # Update the piece's position
        if to_square.occupying_piece:
            to_square.occupying_piece.pos = to_square.pos

        # Switch turns
        self.turn = 'black' if self.turn == 'white' else 'white'

        return True  # Move was successful

    def is_empty(self, pos):
        x, y = pos
        return self.get_square((x,y)).occupying_piece is None

    def is_enemy(self, pos, color):
        square = self.get_square(pos)
        
        # Check if the square exists and has a piece
        if square is None or square.occupying_piece is None:
            return False  # Not an enemy if there's no piece
        
        # Check if the piece on the square is an enemy
        return square.occupying_piece.color != color
    
        
    def get_square_from_pos(self, pos: tuple[float, float]) -> SmSq:
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square

    def get_piece_from_pos(self, pos: tuple[float, float]) -> SimulationPiece:
        return self.get_square_from_pos(pos).occupying_piece

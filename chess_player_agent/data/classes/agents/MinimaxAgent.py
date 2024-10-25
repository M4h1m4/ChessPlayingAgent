# /* MinimaxPlayer.py

from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent
from data.classes.Simulation import SimulationBoard, SmSq
from data.classes.Square import Square
import random

color_code = { # to shorten the color code
            "black": "bl",
            "white": "wh"
        }

point_map = {
            " ": 0,
            "P": 1, #pawn
            "N": 3, #Knight
            "B": 3, #Bishop
            "R": 5, #Rook
            "Q": 9, #Queen
            "K": "INF" #King
        }

class MinimaxAgent(ChessAgent):
    @staticmethod
    #A simulation board is created to make sure minimax agent can move the pieces 
    # andevaluate the best possible move. One alternatives was creating the copy of board
    # However the challenge was to copy of the board which is created from copy is a shallow copy
    def sm_sq_to_sq(sim_square: SmSq, board: Board) -> Square:
        position = sim_square.pos
        return board.get_square_from_pos(position)

    def choose_action(self, board: Board, verbose: bool = True):
        best_move = None
        best_value = float('-inf') # setting the best value to least so that it can be updated later

        sim_bd = SimulationBoard() # a simulation board is being created 
        sim_bd.copy_from_board(board)
        possible_move = self.get_all_possible_moves(sim_bd, self.color)

        random.shuffle(possible_move)

        for move in possible_move:
            sim_bd.handle_move(move['curr_pos'], move['next_pos'])
            mv_value = self.minimax(sim_bd, 
                                      depth=3, 
                                      alpha=float('-inf'), 
                                      beta=float('inf'), 
                                      maximizing_player=False)
            if mv_value > best_value:
                best_value = mv_value
                best_move = (move['start'], move['end'])
        
        # Convert the best move's SimulationSquare to Square before returning
        if best_move:
            start_square = self.sm_sq_to_sq(best_move[0], board)
            end_square = self.sm_sq_to_sq(best_move[1], board)
            return (start_square, end_square)

        return False

    # def print_possible_moves(self, possible_moves):
    #     print("\n###################################")
    #     print("-------------  MOVES --------------\n")
    #     for move in possible_moves:
    #             print("-----------------------------")
    #             print("curr_pos: ", move["curr_pos"])
    #             print("curr_piece", move["curr_piece_color"], move["curr_piece_notation"])
    #             print("next_pos: ", move["next_pos"])
    #             print("next_piece: ", move["next_piece_color"], move["next_piece_notation"])
    #             print("can_capture: ", move["can_capture"])
    #             print("points: ", move["points"])
    #     print()
    
    def evaluate_board(self, board: Board): #Function to evaluate board
        point_map = {
            "P": 1,
            "N": 3,
            "B": 3,
            "R": 5,
            "Q": 9,
            "K": 0  # King will not be considered for evaluation as the end goal is to take down the king
        }

        score = 0
        for sq in board.squares:
            if sq.occupying_piece:
                piece = sq.occupying_piece
                piece_value = point_map.get(piece.notation.upper(), 0)
                score += piece_value if piece.color == self.color else -piece_value

        return score

    def get_all_possible_moves(self, board: SimulationBoard, color: str):
        possible_moves = []

        checkmate_st = self.is_in_checkmate(board, color)# helps to get the status of checkmate
        check_st,threat_piece = self.is_in_check(board,color)# helps to get the status of check

        # check if board is in checkmate
        if checkmate_st:
            return []
        elif check_st:
            
            king_defenses = self.exit_with_king(board, color)
            other_defenses = self.exit_with_piece(board, color, threat_piece)

            defenses = king_defenses
            defenses.extend(other_defenses)
            return defenses

        # general case
        for sq in board.squares:
            if sq.occupying_piece is not None:
                if sq.occupying_piece.notation != ' ':
                    if sq.occupying_piece.color == color:
                        for target in sq.occupying_piece.get_valid_moves(board):
                            can_capture = False
                            points = point_map[" "]

                            if not isinstance(target,SmSq):
                                target_square = board.get_square(target)
                            else:
                                target_square = target

                            if target_square.occupying_piece != None:
                                if target_square.occupying_piece.color != self.color:
                                    can_capture = True
                                    points = point_map[target_square.occupying_piece.notation]

                            possible_moves.append({
                                "start":sq,
                                "curr_pos": sq.pos,
                                "curr_piece_color": color_code[sq.occupying_piece.color] if sq.occupying_piece else None,
                                "curr_piece_notation": sq.occupying_piece.notation if sq.occupying_piece else None,
                                "end": target_square,
                                "next_pos": target_square.pos,
                                "next_piece_color": color_code[target_square.occupying_piece.color] if target_square.occupying_piece else None,
                                "next_piece_notation": target_square.occupying_piece.notation if target_square.occupying_piece else None,
                                "can_capture":can_capture,
                                "points": points
                            })
        return possible_moves

    def get_opponent_color(self):
        return "black" if self.color == "white" else "white"
    
    def minimax(self, board: SimulationBoard, depth: int, alpha: int, beta: int, maximizing_player: bool) -> int:
        if depth == 0:
            return self.evaluate_board(board)

        # Determine the color for the current maximizing or minimizing player
        color = self.color if maximizing_player else self.get_opponent_color()

        # Get all possible moves for the current player
        possible_moves = self.get_all_possible_moves(board, color)
        random.shuffle(possible_moves)

        if maximizing_player:
            max_eval = float('-inf')
            for move in possible_moves:
                board_copy = SimulationBoard()
                board_copy.copy_from_board(board)
                board_copy.handle_move(move['curr_pos'], move['next_pos'])
                eval = self.minimax(board_copy, depth - 1, alpha, beta, False)  # Recurse with minimizing player
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:
            min_eval = float('inf')
            for move in possible_moves:
                board_copy = SimulationBoard()
                board_copy.copy_from_board(board)
                board_copy.handle_move(move['curr_pos'], move['next_pos'])
                eval = self.minimax(board_copy, depth - 1, alpha, beta, True)  # Recurse with maximizing player
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval

    def is_in_check(self, board: SimulationBoard, color: str) -> bool:
        """
        Returns True if the player with the given color is in check.
        """
        king_square = None
        for square in board.squares:
            if square.occupying_piece and \
                square.occupying_piece.color == color and \
                    square.occupying_piece.notation == 'K':
                king_square = square
                break

        if king_square:
            # Check if any opposing piece can move to the king's position
            opponent_color = self.get_opponent_color() if color == self.color else self.color
            for square in board.squares:
                if square.occupying_piece and square.occupying_piece.color == opponent_color:
                    valid_moves = square.occupying_piece.get_valid_moves(board)
                    if king_square in valid_moves:
                        return True, square
        return False, None

    def is_in_checkmate(self, board: SimulationBoard, color: str) -> bool:
        
        # Returns True if the player with the given color is in checkmate.

        is_checked = False # setting the value to false
        king_sq = None
        for sq in board.squares:
            if sq.occupying_piece and sq.occupying_piece.color == color and sq.occupying_piece.notation == 'K':
                king_sq = sq #getting the position of the king
                break

        if king_sq:
            # Checking if any opponent's piece can take down king by moving to its position
            opponent_color = self.get_opponent_color() if color == self.color else self.color
            for sq in board.squares:
                if sq.occupying_piece and sq.occupying_piece.color == opponent_color:
                    valid_moves = sq.occupying_piece.get_valid_moves(board)
                    if king_sq in valid_moves:
                        is_checked = True
        
        if is_checked == False:
            return False
    
        # return safe moves
        safe_moves = []

        king_sq = self.get_king(board, color)
        kings_moves = king_sq.occupying_piece.get_valid_moves(board)


        all_opponent_moves = []
        for square in board.squares:
            if square.occupying_piece is not None:
                if square.occupying_piece.color != color:
                    # look for opponent pieces only
                    all_opponent_moves.append(square.occupying_piece.get_valid_moves(board))

        for move in kings_moves:
            if move not in all_opponent_moves:
                safe_moves.append(move)

        if len(safe_moves)==0:
            return True
        return False

    def get_king(self, board: SimulationBoard, color):
        for sq in board.squares:
            if sq.occupying_piece is not None:
                if sq.occupying_piece.notation == 'K' and sq.occupying_piece.color == color:
                    return sq
    
    def exit_with_king(self, board: SimulationBoard, color):
            safe_moves = []

            king_sq = self.get_king(board, color)
            kings_moves = king_sq.occupying_piece.get_valid_moves(board)

            all_opponent_moves = []
            for sq in board.squares:
                if sq.occupying_piece is not None:
                    if sq.occupying_piece.color != color:
                        # look for opponent pieces only
                        moves_list = sq.occupying_piece.get_valid_moves(board)
                        all_opponent_moves.extend(moves_list)

            for move in kings_moves:
                if move not in all_opponent_moves:
                    can_capture = False
                    points = point_map[" "]

                    # check if the move leads to any captures
                    if move.occupying_piece is not None:
                        if move.occupying_piece.color != self.color:
                            can_capture = True
                            points = point_map[move.occupying_piece.notation]

                    safe_moves.append({
                                "start":king_sq,
                                "curr_pos": king_sq.pos,
                                "curr_piece_color": color_code[king_sq.occupying_piece.color] if king_sq.occupying_piece else None,
                                "curr_piece_notation": king_sq.occupying_piece.notation if king_sq.occupying_piece else None,
                                "end": move,
                                "next_pos": move.pos,
                                "next_piece_color": color_code[move.occupying_piece.color] if move.occupying_piece else None,
                                "next_piece_notation": move.occupying_piece.notation if move.occupying_piece else None,
                                "can_capture":can_capture,
                                "points": points
                            })

            #print("safe moves:", [(move["curr_pos"], move["next_pos"]) for move in safe_moves])
            # Just to debug, adding this is aking th game slow
            return safe_moves

    def exit_with_piece(self,
                                        board: SimulationBoard,
                                        color,
                                        threat_piece: SmSq):

        threat_moves = threat_piece.occupying_piece.get_valid_moves(board)

        # print(threat_piece.occupying_piece.notation)
        # print("threat_moves:" , [(threat_piece.occupying_piece.pos, move.pos) for move in threat_moves])

        defense_moves = []
        all_possible_moves = []
        for square in board.squares:
            if square.occupying_piece is not None:
                if square.occupying_piece.notation != ' ' and \
                    square.occupying_piece.notation != "K" and \
                        square.occupying_piece.color == color:
                    all_possible_moves.extend(square.occupying_piece.get_valid_moves(board))
        
        for defense in defense_moves:
            if defense in threat_moves:
                defense_moves.append(defense)    

        # print("defense moves:", [(move["curr_pos"], move["next_pos"]) for move in defense_moves])

        return defense_moves

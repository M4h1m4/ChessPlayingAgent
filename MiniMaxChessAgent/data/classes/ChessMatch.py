import pygame
from data.classes.Board import Board
from data.classes.agents.ChessAgent import ChessAgent
from matplotlib import pyplot as plt
import time

def chess_match(white_player: ChessAgent, black_player: ChessAgent):
    assert(white_player.color == 'white')
    assert(black_player.color == 'black')
    pygame.init()
    WINDOW_SIZE = (600, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    board = Board(screen, WINDOW_SIZE[0], WINDOW_SIZE[1])
    agents: list[ChessAgent] = [white_player, black_player]
    i: int = 0
    moves_count: int = 0
    winner = None

    # Run the main game loop
    running = True
    while running:
        print(f"Current Turn: {board.turn}")  # Show current turn
        chosen_action = agents[i].choose_action(board)

        if chosen_action is False or moves_count > 1000:
            print('Players draw!')
            running = False
        else:
            print("Chosen action:", chosen_action[0].pos, chosen_action[1].pos)  #Show chosen action
            # Check if the move is valid before applying it
            if board.handle_move(*chosen_action):
                moves_count += 1
                i = (i + 1) % len(agents)  # Switch turns only on valid move
                # Check for checkmate after a valid move
                if board.is_in_checkmate(board.turn):
                    if board.turn == 'white':
                        winner='black'
                        print('Black wins!')
                    else:
                        winner='white'
                        print('White wins!')
                    running = False
            else:
                print("Invalid move!")  # Notify about invalid moves
                #break
                continue
        board.draw()

    #return winner



    # Allow the player to view the result
    viewing = True
    while viewing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                viewing = False
    return winner

def run_experiments(minimax_agent, opponent_agent, iterations=10):
    results = {'minimax': 0, 'opponent': 0, 'draw': 0}
    for _ in range(10):
        winner = chess_match(minimax_agent, opponent_agent)
        if winner == 'white' and minimax_agent.color == 'white':
            results['minimax'] += 1
        elif winner == 'black' and minimax_agent.color == 'black':
            results['minimax'] += 1
        elif winner == 'draw':
            results['draw'] += 1
        else:
            results['opponent'] += 1

    return results

def plot_win_rate(results):
    labels = ['Minimax Wins', 'Opponent Wins', 'Draws']
    values = [results['minimax'], results['opponent'], results['draw']]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['green', 'red', 'gray'])
    plt.title('Minimax Agent Win Rate over 10 Games')
    plt.ylabel('Number of Games')
    plt.show()


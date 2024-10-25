## Assignment Description
Your task is to write an agent inheriting from `ChessAgent` based on the methods discussed in class. You pay place your agent `.py` file in `data/classes/agents/`, where you will also find the `HumanPlayer` and `RandomPlayer` for reference. Like the previous assignment, you must collect data on the performance of your agent over at least 100 matches. It is suggested that you use the `chess_match` function as demonstrated in `main.py` and write your own script which uses your agent over those 100 matches.

## Setup Instructions
You can install the requirements (only pygame) by running `pip install -r requirements.txt`

Then you can run the program with `python main.py HumanPlayer RandomPlayer` to have a human play as white by selecting which pieces to move against an agent which chooses its moves randomly. You can choose both as `HumanPlayer` for both black and white players to be human-controlled

## Game Details
In general, the player can choose into which type of piece the pawn promotes. For simplicity, when a pawn reaches the end of the board in this version of the game, it automatically promotes to a queen piece. Another rule of chess is that if both players repeat the same move 3 times in a row, the game is a draw. To prevent games between `RandomPlayer`s taking forever, we instead declare a draw after 1000 total moves is neither player has won.

When one of the players wins by checkmating the opponent's King, the message "White/Black wins!" will be printed in the terminal and no more moves can be played

As a human player, you can click on any of your pieces and be shown in green to which squares that piece can move (which do not cause you to be in check). Click any square which is not highlighted to stop showing the valid moves for that piece.

## Credits
This assignment is adapted from the following tutorial for coding chess in python.

https://thepythoncode.com/article/make-a-chess-game-using-pygame-in-python

The images used for the chess pieces are taken from the wikimedia foundation.

https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
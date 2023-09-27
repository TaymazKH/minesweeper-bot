# start
START = '''
<b>Welcome to the {bot_name} bot!</b>
A fun and fast-paced 2 player minesweeper game

<b>Quick Start</b>
Just type @{bot_username} and press the button that appears above the text area to send a match request.
If someone presses the "play" button, they become your rival and the game begins!

<b>How to play</b>
The game area is a rectangular map and there are mines hidden in some cells.
Your goal is to find more mines than your rival.
On their turn, a player chooses an unrevealed cell to open it.
If it's a mine, then they gain a score and can continue their turn.
But if it's not a mine, then their turn ends and a number is revealed in that cell.
Each number indicates the number of mines in the surrounding 8 cells.
If the number of the chosen cell is 0, then all the surrounding cells are revealed as well.

<b>Custom Game</b>
You can customize the size of the map and the number of mines in it.
After typing @{bot_username}, you must enter 3 integers each separated with a space.
Example: <code>@{bot_username} 7 6 15</code>
This will generate a map with 7 rows, 6 columns and 15 mines.
The default values are 8, 8 and 21.
'''

# query
INVALID_INLINE_FORMAT = '''
<b>Invalid Inline Query Format</b>
After typing @{bot_username}, you must either not type anything or enter 3 integers each separated with a space.
Example: <code>@{bot_username}</code>
Example: <code>@{bot_username} 7 6 15</code>
'''
INVALID_INLINE_ARGS = '''
<b>Invalid Inline Query Arguments</b>
There are some constraints that apply to height, width, and the number of mines:
{c1} 5 <= Width <= 8.
{c2} 5 <= Height <= 11.
{c3} Number of cells <= 95.
{c4} 7 <= Number of mines <= number of cells.
{c5} Number of mines must be an odd number.
'''

# game
LETS_PLAY = '''
Let's play a game of minesweeper!
Who wants to play against me?
'''
GAME = '''
Players: {player1} 🔴 🔵 {player2}
Scores: {score1} 🔴 🔵 {score2}
Turn: {current_player}
Mines left: {mines_left}
'''
WIN = '''
Winner: 🏅 {winner}
Scores: {score1} 🔴 🔵 {score2}
'''

# alert
CANT_PLAY_WITH_YOURSELF = "You can't play against yourself!"
NOT_YOUR_TURN = "It's not your turn! Or maybe you're not a player?!"
ALREADY_REVEALED = "That cell is already revealed! select an unrevealed one!"

# chat

# error
UNKNOWN_ERROR = 'An unknown error has occurred!'

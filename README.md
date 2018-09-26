# Bagh-Chal
Bag-Chal is the 2-player strategic board game consisting of tigers and goats originated in Nepal.  Played on 5 by 5 grid, the game has 20 goats and 4 tigers in the starting of the game.  Tigers aim to capture the goat and goat aim to restrict legal movement of tiger.  When none of the tigers are given legal movement, goats win whereas death of 5 goats make the tiger winner.
Regarding rules and more information of Bag-Chal, please [click here](https://en.wikipedia.org/wiki/Bagh-Chal).

## About This Repository:
The Bagh-Chal game here is built in Python using Tkinter GUI library.  Here, users can play with computer either as tiger or goat at different difficulty.  For AI, we have implemented minimax algorithm with alpha beta pruning.

## Dependencies
The only dependency as of now is tkinter.  Install tkinter by executing the following commands in the terminal.
```
$ sudo apt-get update
$ sudo apt-get install python3-tk
```

## Usage
First clone the repository.
```
git clone https://github.com/code-geek/pybaghchal
```
Then, go to the project directory and run ui.py.
```
cd baghchal (if name of project directory is baghchal)
./ui.py
or python3 ui.py
```

The code here is modular so as to make it readable and easy to maintain.
The modules serves different purpose as follows:
- Board.py: Module describing board parameters and methods.
- Engine.py: Module containing AI engine for the game.
- Game.py: Module that lets us play the game in terminal.  This helps for the game to be integrated across different other platforms.
- Point.py: Module containing class for the point.  It contains helper methods and attributes that a point in Bagh-Chal board game represents.
- tests.py: Testing module using unittest python module.
- ui.py: UI created using tkinter and imports AI logic from Engine.py.  Board logic is imported from Board.py.
- ui.conf: Configuration file for playing options as goat/tiger and level of difficulty.

## Further Improvements:
- The entire code is written in Python so in higher difficulty(which mean higher depth so higher computation time), the AI takes long time to make the move.  We could implement AI engine using low level programming language(like C++).  That helps a lot to make the AI make move faster.
- We have used minimax algorithm with alpha beta pruning for AI implementation.  We could use reinforcement learning further to make stronger AI.

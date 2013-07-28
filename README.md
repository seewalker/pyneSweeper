pyneSweeper
===========

A Minesweeper Clone                                                  
                                             
## Usage

   To play this minesweeper clone, run the script 'game.py' with two command 
line arguments: the name which the score will be associated with in score logging and 
the difficulty. The set of difficulty options is currently (Easy, Regular, Difficult,
Expert). 

   To see a summary of game statistics, run the script 'stats.py' with the username
in question as the command line argument. 

## Screenshots
When the game is ongoing...

![Midgame](https://raw.github.com/seewalker/pyneSweeper/master/images/Midgame.png)

When the game ends in defeat...

![Defeat](https://raw.github.com/seewalker/pyneSweeper/master/images/Defeat.png)

When the game ends in victory...

![Victory](https://raw.github.com/seewalker/pyneSweeper/master/images/Victory.png)

## Dependencies
a shell such as bash, zsh, tcsh.

python 2.x

pygame

## Unique Features of This Implementation
1. It is impossible to lose on the first sweep. This is accomplished by defining
the bomb locations after the first sweep. I consider this to be a quality design
feature because there is little rhyme-or-reason to the first choice. 

2. Recursive sweeping of cells with zero adjacent bombs. 

3. Pythonic aesthetics in the naming of the classes and the appearance of the
game.

4.  Depending on the state of the hasBoarders variable in platonic.boardParams,
the board does or does not have visual edges between the cells. This is done
by either making the cell size either small enough to preserve the backbround
color from the initital rendering or by making the cells a bit bigger. That
difference is made by the offset variable in the game.drawCells function.

5. In the spirit of object-oriented architecture, the core logic of the game
is separated from the state of the game which are separated from the visual
appearance of the game. The core logic is specified in platonic.essence. The
parameters that determine the definitions of the difficulty levels (and the 
named constants which map to these levels) are in the gameParams class. The
game state 

## Explanations of Possibly Weird Design Choices
0. A cell is swept upon the BUTTONUP event rather than the BUTTONDOWN event. 
It is so because the user may notice, between depressing and releasing the 
mouse button, that he or she meant to click on a different cell. 

1. Why don't the functions that map something to something else, such
as mapToCell, pass a tuple and thereby be more concise? I chose to make x 
and y coordinates separate parameters so that I need not have a line that looks
like "x, y = arg[0], arg[1]". Without this extra line, those functions can be
one liner functions that consist soley of a return expression (which is elegant). 

2. If something else seems weird, let me know! My email address is
seewalker.120@gmail.com.

## Things To Come (Maybe)

0. The four difficulty levels and the density of bombs for each difficulty 
level are chosen arbitrarily. It would be better if these design decisions were
more systematic.

1. In the course of playing Minesweeper, there are times where one cannot 
sweep a cell with certainty. Those of us who like minimal chance in their games
it would be beneficial to have a mode where these fifty-fifty situations are
automatically resolved.

2. A Minesweeper solution engine. This is probably a superset of the item above.

3. A button to initiate a new game, rather than restarting every time from the
command line.

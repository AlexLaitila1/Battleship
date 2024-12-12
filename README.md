# Battleship
A project done during my first year of university. A simple battleship game
based on another text document that contains the name and the coordinates of 
the ships.

Game manual / description:

Before you start:
You need to have downloaded a text document and boat.gif file. Make sure they
all are in the same folder. The text document(.txt) needs to have at least one
ship in it and coordinates for it.
It needs to be in a format, (NAME;COORDINATE;COORDINATE...) and the next ship
needs to be in a new row. Coordinates need to be uppercase letter and a number.
The ships coordinates cannot overlap with each other.
Example of a ship: (Ship;A1;A2)

How to play:
When you run the program, the game asks for you to enter the name of the ship
file. Then you press "Start Game" -button and the program checks if the file
is usable. If the file is invalid, the program clears the entry slot and asks
for a new file. If you try to leave the entry slot empty, the program does not
continue and asks for you to enter a filename. After that the program creates a
game board where there are different coordinate buttons. You can guess a
coordinate by clicking the corresponding coordinate. The game gives you a "*",
if the guess was wrong and an "X" if it hit a ship. Once you have guessed all
the ships coordinates, the program tells you "you have sunk a (name)" and swaps
all the "X" to the first letter of the ships name. You cannot guess the same
coordinate twice. The program tells you that you've already guessed the
coordinate.
Once you have sunk all the ships, the program opens a new user interface where
you can play again or quit.

The program also has a menu on the top left of the window on Windows and on Mac
it is on top of the screen where you can restart at any time or quit the game.
By restarting the game, the program closes itself and creates a new game.
You can also adjust the size of the window at any time.

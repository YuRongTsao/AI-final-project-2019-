# Two player board game
Design an AI program to play a two-player nXn board game with human player or the other AI program.

## Description
### Introduction
Take a 4X4 board for example:

![image](./img/png1.png)

Each tile is colored in Red (denoted by R) or Blue (denoted by B), and the numbers of the color tiles are even, e.g. 8 Red and 8 Blue on a 4X4 board.

You can choose R or B first, and then you can choose to make the 1st move or the next.
Each single move involves the removal of a colored tile of the choice. For example, given the initial board configuration above, assuming your color is R, and you’ll make the 1st 
move, one possible legal move will be removing the R on the upper left corner. The new board configuration is shown below after you remove that R.

![image](./img/png2.png)

This is a two-player game that takes alternating turns. After your move, it is the AI program’s turn to make its move, e.g. removing the B on the low left corner. Now the new board 
configuration becomes

![image](./img/png3.png)

The one that removes all the colored tiles of the choice first is the winner. In this example, if you remove all the R’s before the AI removes all the B’s, you win.
At this point, the game may look naïve because whoever makes the 1st move is guaranteed to win. Nevertheless, there are other rules of the game, as detailed below, that make this 
game a bit more complicated.

### Rules
1. The removal of a tile will cause side effects that apply ONLY to its “direct” neighbors regardless of their colors.
E.g. the removal of the R will affect its direct neighbors right above, right below, to its left, and to its right (as indicated by the four question marks).

![image](./img/png4.png)
![image](./img/png5.png)
![image](./img/png6.png)

2. The side effects can cause the automatic removals of these direct neighbors under certain conditions. 
Each tile (as a square) has 4 sides. After a tile is removed, you need to check its direct neighbors. Depending on its location on the board, it can have at most 
4 direct neighbors (note. the colors of neighbors do not matter). For each of these neighbors, unless it has three or four sides connected to other tiles or to the 
wall (side) of the board, it will be removed automatically.

![image](./img/png7.png)

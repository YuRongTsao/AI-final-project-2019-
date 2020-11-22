# Two player board game
* Design an AI program to play a two-player nXn board game with human player or the other AI program.
* Use MCTS(monte carlo tree search) to find the next step of AI program.

## Description
### Introduction
Take a 4X4 board for example:

![Fig1](./img/fig1.PNG)

Each tile is colored in Red (denoted by R) or Blue (denoted by B), and the numbers of the color tiles are even, e.g. 8 Red and 8 Blue on a 4X4 board.

You can choose R or B first, and then you can choose to make the 1st move or the next.
Each single move involves the removal of a colored tile of the choice. For example, given the initial board configuration above, assuming your color is R, and you’ll make the 1st 
move, one possible legal move will be removing the R on the upper left corner. The new board configuration is shown below after you remove that R.

![Fig2](./img/fig2.PNG)

This is a two-player game that takes alternating turns. After your move, it is the AI program’s turn to make its move, e.g. removing the B on the low left corner. Now the new board 
configuration becomes

![Fig3](./img/fig3.PNG)

The one that removes all the colored tiles of the choice first is the winner. In this example, if you remove all the R’s before the AI removes all the B’s, you win.
At this point, the game may look naïve because whoever makes the 1st move is guaranteed to win. Nevertheless, there are other rules of the game, as detailed below, that make this 
game a bit more complicated.

### Rules
1. The removal of a tile will cause side effects that apply ONLY to its “direct” neighbors regardless of their colors.
E.g. the removal of the R will affect its direct neighbors right above, right below, to its left, and to its right (as indicated by the four question marks).

![Fig4](./img/fig4.PNG)
![Fig5](./img/fig5.PNG)
![Fig6](./img/fig6.PNG)

2. The side effects can cause the automatic removals of these direct neighbors under certain conditions. 
Each tile (as a square) has 4 sides. After a tile is removed, you need to check its direct neighbors. Depending on its location on the board, it can have at most 
4 direct neighbors (note. the colors of neighbors do not matter). For each of these neighbors, unless it has three or four sides connected to other tiles or to the 
wall (side) of the board, it will be removed automatically.

![Fig7](./img/fig7.PNG)

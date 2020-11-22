# Two player board game
* Design an AI program to play a two-player nXn board game with human player or the other AI program.
* Use **MCTS(monte carlo tree search)** to find the next step of AI program.

## Description
### Introduction
Take a 4X4 board for example:

<p align="center">
  <img src="./img/fig1.PNG">
</p>

Each tile is colored in Red (denoted by R) or Blue (denoted by B), and the numbers of the color tiles are even, e.g. 8 Red and 8 Blue on a 4X4 board.

You can choose R or B first, and then you can choose to make the 1st move or the next.
Each single move involves the removal of a colored tile of the choice. For example, given the initial board configuration above, assuming your color is R, and you’ll make the 1st 
move, one possible legal move will be removing the R on the upper left corner. The new board configuration is shown below after you remove that R.

<p align="center">
  <img src="./img/fig2.PNG">
</p>

This is a two-player game that takes alternating turns. After your move, it is the AI program’s turn to make its move, e.g. removing the B on the low left corner. Now the new board 
configuration becomes

<p align="center">
  <img src="./img/fig3.PNG">
</p>

The one that removes all the colored tiles of the choice first is the winner. In this example, if you remove all the R’s before the AI removes all the B’s, you win.
At this point, the game may look naïve because whoever makes the 1st move is guaranteed to win. Nevertheless, there are other rules of the game, as detailed below, that make this 
game a bit more complicated.

### Rules
1. The removal of a tile will cause side effects that apply ONLY to its “direct” neighbors regardless of their colors.
E.g. the removal of the R will affect its direct neighbors right above, right below, to its left, and to its right (as indicated by the four question marks).

<p align="center">
  <img src="./img/fig4.PNG">
  <img src="./img/fig5.PNG">
  <img src="./img/fig6.PNG">
</p>


2. The side effects can cause the automatic removals of these direct neighbors under certain conditions. 
Each tile (as a square) has 4 sides. After a tile is removed, you need to check its direct neighbors. Depending on its location on the board, it can have at most 
4 direct neighbors (note. the colors of neighbors do not matter). For each of these neighbors, unless it has three or four sides connected to other tiles or to the 
wall (side) of the board, it will be removed automatically.

<p align="center">
  <img src="./img/fig7.PNG">
</p>

## Build the AI program
In order to find the next step of the AI program, we used **MCTS(monte carlo tree search)** as the search strategy.

### What is MCTS
This algorithm is used specially in games, Alpha Go reportedly used this algorithm with a combination of Neural Network. 

MCTS is a way of searching a tree. Within this tree, its nodes represent the **states** and the arc between nodes represents the **choice** that would take from one state to the other. 

The algorithm consists of 3 phases:

**1. Selection**



### Applying MCTS in this game
In this project, the **board** represent the state and each **tile** represents the choice that AI program would take.


The search procedure consists of 3 phases, **Tree policy,Default policy,and Backpropagation**




**Tree policy (Selection)**

**Default policy (Rollout)**


Repeat the above mentioned procedure with `k iterations (k=1000)`, the AI program will choose a best tile to be removed based on the UBC function.  

*Note: adjust variable `k` in `AILoop()` function can change the number of iteration of the MCTS algorithm.*

*Note: change the `fileName` to change initial board*

## Play the game with AI program
**Step 1**

Run the `final_project.py`, you will see a initial board with the color of each tile and the number of rows and columns.

<p align="center">
  <img src="./img/fig8.PNG">
</p>

**Step 2**

Users can choose if they want to go first or not, and they have to select a color.
Enter the number of row and column to remove the tile, the console will first show the board after users remove the specific tile and then show the board after the side effect.

<p align="center">
  <img src="./img/fig9.PNG">
</p>

**Step 3**

The AI program will decide it's action right after the user turn. The console will also show two boards, the first is the current board after the AI remove the tile, and the second board is the result of the side effect.

<p align="center">
  <img src="./img/fig10.PNG">
</p>

**Step 4**

Users can choose their next step to remove the tile. Repeat the above steps, which is, the AI program and the user take turns to remove the tile, until the end of the game

<p align="center">
  <img src="./img/fig11.PNG">
</p>

**Reference**
[AI: Monte Carlo Tree Search (MCTS)](https://medium.com/@pedrohbtp/ai-monte-carlo-tree-search-mcts-49607046b204) 

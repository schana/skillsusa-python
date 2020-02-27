# SkillsUSA Programming Contest - Python edition

This repository houses the code for contestants to build their own Snake AI.

## Requirements

1. Implement a SnakeMover as described in [Getting Started](#getting-started).
1. Write a short explanation describing how your snake chooses to move.

## Contest Rules

1. Don't copy code from the internet. Your code should be your original work.
1. You can reference the following sites freely
   * [Python API Documentation](https://docs.python.org/3.7/)
   * [Wikipedia](https://en.wikipedia.org/wiki/Main_Page)
1. Asking for help is encouraged. This is primarily a learning experience.
1. Have fun :)

## Game Rules
This game of snake takes place on a fixed game board. The snake can move in any direction, but will die if it touches a wall or itself. If it touches a piece of food, its length will increase by one.

Each game is limited to 1000 moves.

### Game Board

Our game board is a 10x10 grid referenced by a `(row, column)` tuple. This is represented by the `Cell` object in the code. Notice the indexing starts at zero in the upper left corner. The directions the snake can move are in relation to this board.

|   |   |   |   |   |   |
|:---:|:---:|:---:|:---:|:---:|:---:|
|(0,0)|(0,1)|(0,2)|...|(0,8)|(0,9)|
|(1,0)|(1,1)|(1,2)|...|(1,8)|(1,9)|
|(2,0)|(2,1)|(2,2)|...|(2,8)|(2,9)|
|...|...|...|...|...|...|
|(8,0)|(8,1)|(8,2)|...|(8,8)|(8,9)|
|(9,0)|(9,1)|(9,2)|...|(9,8)|(9,9)|

### Scoring

Your snake will be scored on how many pieces of food it eats in the allotted time. It will be run a million times using randomly generated starting and food locations. The highest average score will be the winner, with ties decided by having the lower average age. Further ties will be decided by correctness of program, completeness, explanation, and overall quality of work.

## Getting Started

Your goal is to implement the `get_next_direction()` function in `mover.py`. `SnakeMover` has access to the `board` module, which contains all the relevant state of the game. The `examples` module has some completed solvers for inspiration.

### Moving algorithms

There are many different correct approaches you can take to solve the task. Here are some additional options:

#### Hamilton

The goal of this algorithm is to establish a complete cycle (as has been done in `CompletionistMover`). Unfortunately, this type of snake takes too long to win the game, typically between 2000-3000 moves. We can improve this strategy by allowing the snake to take shortcuts. The snake can take a shortcut in the cycle so long as the head of the snake doesn't overtake the tail.

1. https://en.wikipedia.org/wiki/Hamiltonian_path
1. https://en.wikipedia.org/wiki/Hamiltonian_path_problem

#### Greedy

This solver tries to eat the food as quickly as possible. It tries to establish a safe path between the food and itself. If such a path exists, it travels along it. Otherwise, it wanders around in the free spaces until such a path becomes available. These steps are accomplished by using algorithms to compute both the shortest path and longest path: shortest for finding the safe path between the food and itself, and longest for deciding how to wander.

1. https://en.wikipedia.org/wiki/Greedy_algorithm

#### A* search

This is an algorithm that searches paths for a goal by establishing a set of neighbors, determining which are closest to the goal, and then exploring their neighbors. Each new neighbor keeps track of where it came from. This process continues until the goal is reached, and then the neighbors are tracked back to establish a path.

![A star animation](https://upload.wikimedia.org/wikipedia/commons/5/5d/Astar_progress_animation.gif)

1. https://en.wikipedia.org/wiki/A_star_search_algorithm

### Path solvers

The following algorithms can be used to search out possible paths for the snake to travel along.

#### Shortest path

1. https://en.wikipedia.org/wiki/Breadth-first_search

#### Longest path

1. https://en.wikipedia.org/wiki/Longest_path_problem
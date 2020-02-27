import itertools
import random

from game import board
from game import cell, mover as m
from game.internal import body
from game.internal import snake

cells = {cell.Cell(r, c) for r, c in itertools.product(range(board.ROWS), range(board.COLUMNS))}
food = None
age = 0
mover = m.SnakeMover()


def reset():
    global food, age
    body.initialize(cell.Cell(random.randint(0, board.ROWS - 1), random.randint(0, board.COLUMNS - 1)))
    snake.mover = mover
    snake.alive = True
    food = get_random_free_cell()
    set_board()
    age = 0


def set_board():
    board.body = snake.body.cells[:]
    board.food = food


def step():
    global age, food
    age += 1
    snake.move(food)
    if snake.consumed_food:
        next_food = get_random_free_cell()
        if next_food:
            food = next_food
        else:
            return False
    set_board()
    return snake.alive


def get_score():
    return len(snake.body.cells)


def get_random_free_cell():
    food_options = tuple(cells.difference(set(snake.body.cells)))
    if food_options:
        return random.choice(food_options)
    else:
        return None

import itertools
import random

from game import cell, mover
from game import board
from game.internal import snake


class GameState:
    snake = None
    food = None
    age = 0

    def __init__(self, b):
        self.board = b
        self.cells = {cell.Cell(r, c) for r, c in itertools.product(range(board.ROWS), range(board.COLUMNS))}
        self.reset()

    def reset(self):
        self.snake = snake.Snake(head=cell.Cell(random.randint(0, board.ROWS), random.randint(0, board.COLUMNS)),
                                 mover=mover.SnakeMover(self.board))
        self.food = self.get_random_free_cell()
        self.set_board()
        self.age = 0

    def set_board(self):
        self.board.body = self.snake.body.cells
        self.board.food = self.food

    def step(self):
        self.age += 1
        self.snake.move(self.food)
        if self.snake.consumed_food:
            next_food = self.get_random_free_cell()
            if next_food:
                self.food = next_food
            else:
                return False
        self.set_board()
        return self.snake.alive

    def get_score(self):
        return len(self.snake.body.cells)

    def get_random_free_cell(self):
        food_options = tuple(self.cells.difference(set(self.snake.body.cells)))
        if food_options:
            return random.choice(food_options)
        else:
            return None

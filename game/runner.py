import random
import json

from game import util
from game import board
from game import snake


class Game:
    def __init__(self, rows, columns, turn_limit=-1, display=True, record=False, delay=0, gui=False):
        self.rows = rows
        self.columns = columns
        self.last_cell = util.Cell(self.rows - 1, self.columns - 1)
        self.turn_limit = turn_limit
        self.board = board.Board(rows=self.rows, columns=self.columns, display=display, record=record, gui=gui)
        self.delay = delay
        self.display = display
        self.record = record
        if self.display:
            self.board.initialize()
        self.snake = None
        self.food = None

    def add_snake(self, name, move_function):
        self.snake = snake.Snake(name, self.get_random_cell(), move_function)

    def get_random_cell(self):
        return util.Cell(random.randint(0, self.last_cell.r), random.randint(0, self.last_cell.c))

    def get_scores(self):
        return {self.snake.name: {'alive': self.snake.alive, 'score': len(self.snake.body), 'age': self.snake.age}}

    def generate_move_parameters(self):
        return {
            'head': {
                'r': self.snake.head.r,
                'c': self.snake.head.c
            },
            'food': {
                'r': self.food.r,
                'c': self.food.c
            },
            'body': [
                {'r': c.r, 'c': c.c} for c in self.snake.body
            ],
            'rows': self.rows,
            'columns': self.columns
        }

    def move(self):
        self.snake.do_move(self.snake.move(json.dumps(self.generate_move_parameters())))
        should_grow = self.food in self.snake.body
        self.snake.advance_tail(should_grow)
        if self.display:
            self.board.fill_cells(self.snake.body, util.Color(180, 180, 180), self.snake.name[0])
        if self.snake.should_die(self.last_cell):
            self.snake.alive = False
            self.board.fill_cells([self.snake.head], util.Color(240, 50, 50))

    def run(self, identifier):
        self.food = self.get_random_cell()
        limit = self.turn_limit
        while self.snake.alive and limit != 0:
            limit -= 1
            self.move()
            if self.snake.alive and self.food in self.snake.body:
                food_options = list(self.board.cells.difference(set(self.snake.body)))
                if food_options:
                    self.food = random.choice(food_options)
                else:
                    print('no free spaces')
                    break
            if self.display:
                self.board.fill_cells([self.food], util.Color(0, 100, 0), '+')
                d = self.delay if self.snake.alive else 1000
                self.board.draw(identifier, self.record, d)
                self.board.clear()

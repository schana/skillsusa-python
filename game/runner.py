import random
import json

from game import util
from game import board
from game import snake


class Game:
    def __init__(self, rows, columns, display=True):
        self.rows = rows
        self.columns = columns
        self.last_cell = util.Cell(self.rows - 1, self.columns - 1)
        self.board = board.Board(rows=self.rows, columns=self.columns)
        self.display = display
        if self.display:
            self.board.initialize()
        self.snakes = []
        self.food = None

    def add_snake(self, name, move_function):
        self.snakes.append(snake.Snake(name, self.get_random_cell(), move_function))

    def get_random_cell(self):
        return util.Cell(random.randint(0, self.last_cell.r), random.randint(0, self.last_cell.c))

    def get_filled_cells(self):
        filled_cells = set()
        for s in self.snakes:
            if s.alive:
                filled_cells.update(set(s.body))
        return filled_cells

    def get_scores(self):
        scores = {}
        for s in self.snakes:
            scores[s.name] = {
                'alive': s.alive,
                'score': len(s.body),
                'age': s.age
            }
        return scores

    def generate_move_parameters(self, current_snake, filled):
        return {
            'head': {
                'r': current_snake.head.r,
                'c': current_snake.head.c
            },
            'food': {
                'r': self.food.r,
                'c': self.food.c
            },
            'body': [
                {'r': c.r, 'c': c.c} for c in current_snake.body
            ],
            'filled': [
                {'r': c.r, 'c': c.c} for c in filled
            ],
            'rows': self.rows,
            'columns': self.columns,
            'data': current_snake.data
        }

    def run(self):
        self.food = self.get_random_cell()
        keep_going = True
        while keep_going:
            keep_going = False
            for s in self.snakes:
                if s.alive:
                    keep_going = True
                    filled_cells = self.get_filled_cells()
                    s.do_move(s.move(json.dumps(self.generate_move_parameters(s, filled_cells))))
                    should_grow = self.food in s.body
                    if should_grow:
                        food_options = list(self.board.cells.difference(filled_cells))
                        if food_options:
                            self.food = random.choice(food_options)
                        else:
                            print('no free spaces')
                            keep_going = False
                    if s.should_die(self.last_cell, filled_cells, should_grow):
                        s.alive = False
                    else:
                        s.age += 1
                        if self.display:
                            self.board.fill_cells([s.head], s.color)
                            for i in range(1, len(s.body)):
                                self.board.fill_cells([s.body[i]], s.color)
            if self.display:
                self.board.fill_cells([self.food], util.Color(0, 100, 0))
                self.board.draw()
                self.board.clear()

import random
import json

from game import util
from game import board
from game import snake


class Game:
    def __init__(self, rows, columns, turn_limit=-1, display=True, record=False, delay=0):
        self.rows = rows
        self.columns = columns
        self.turn_limit = turn_limit
        self.last_cell = util.Cell(self.rows - 1, self.columns - 1)
        self.board = board.Board(rows=self.rows, columns=self.columns)
        self.display = display
        self.record = record
        self.delay = delay
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

    def move_snake(self, s):
        if s.alive:
            filled_cells = self.get_filled_cells()
            s.do_move(s.move(json.dumps(self.generate_move_parameters(s, filled_cells))))
            should_grow = self.food in s.body
            if s.should_die(self.last_cell, filled_cells, should_grow):
                s.alive = False
            else:
                s.age += 1
                if self.display:
                    self.board.fill_cells([s.head], s.color, s.name[0].upper())
                    for i in range(1, len(s.body)):
                        self.board.fill_cells([s.body[i]], s.color, s.name[0])
        else:
            return False
        return True

    def run(self, identifier):
        self.food = self.get_random_cell()
        keep_going = True
        limit = self.turn_limit
        while keep_going and limit != 0:
            keep_going = False
            limit -= 1
            for s in self.snakes:
                keep_going = keep_going and self.move_snake(s)
                if s.alive and self.food in s.body:
                    food_options = list(self.board.cells.difference(self.get_filled_cells()))
                    if food_options:
                        self.food = random.choice(food_options)
                    else:
                        print('no free spaces')
                        keep_going = False
            if self.display:
                self.board.fill_cells([self.food], util.Color(0, 100, 0), '+')
                self.board.draw(identifier, self.record, self.delay)
                self.board.clear()

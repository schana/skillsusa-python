import typing
import random

from game import util
Cell = typing.NewType('Cell', util.Cell)
Cells = typing.Set[util.Cell]


class Snake:
    def __init__(self, name, head: Cell, move_function):
        self.name = name
        self.head = head
        self.body = [self.head]
        self.color = util.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.alive = True
        self.age = 0
        self.data = ''
        self.move = move_function

    def do_move(self, direction):
        if direction == 'u':
            new_head = util.Cell(self.head.r - 1, self.head.c)
        elif direction == 'd':
            new_head = util.Cell(self.head.r + 1, self.head.c)
        elif direction == 'l':
            new_head = util.Cell(self.head.r, self.head.c - 1)
        else:
            new_head = util.Cell(self.head.r, self.head.c + 1)
        self.head = new_head
        self.body.insert(0, self.head)

    def should_die(self, last_cell: Cell, filled_cells: Cells = None, should_grow=False):
        if filled_cells is None:
            filled_cells = set()
        if not should_grow:
            del self.body[-1]
        if len(self.body) != len(set(self.body)):
            return True
        if self.head in filled_cells:
            return True
        if self.head.r < 0 or self.head.c < 0 or self.head.r > last_cell.r or self.head.c > last_cell.c:
            return True
        return False

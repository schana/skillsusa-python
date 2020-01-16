from game import util


class Snake:
    def __init__(self, name, head, move_function):
        self.name = name
        self.head = head
        self.body = [self.head]
        self.alive = True
        self.age = 0
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
        self.age += 1

    def advance_tail(self, should_grow=False):
        if not should_grow:
            del self.body[-1]

    def should_die(self, last_cell):
        if len(self.body) != len(set(self.body)):
            return True
        if self.head.r < 0 or self.head.c < 0 or self.head.r > last_cell.r or self.head.c > last_cell.c:
            return True
        return False

import random

from game import util
from game import board
from game import snake

LAST_CELL = util.Cell(15, 19)
game_board = board.Board(rows=LAST_CELL.r + 1, columns=LAST_CELL.c + 1)
game_board.initialize()
s = snake.Snake(util.Cell(0, 0))
food = util.Cell(5, 5)
high_score = 1
rounds = 0
while True:
    s.do_move(s.move(food, LAST_CELL.c + 1, LAST_CELL.r + 1))
    should_grow = food in s.body
    if should_grow:
        if len(s.body) + 1 >= (LAST_CELL.c + 1) * (LAST_CELL.r + 1):
            print('you win')
            break
        while True:
            food = util.Cell(random.randint(0, LAST_CELL.r), random.randint(0, LAST_CELL.c))
            if food not in s.body:
                break
    if s.should_die(LAST_CELL, should_grow):
        if len(s.body) - 1 > high_score:
            high_score = len(s.body) - 1
            print(high_score)
        rounds += 1
        if rounds % 10 == 0:
            print('r', rounds)
        s = snake.Snake(util.Cell(0, 0))
    game_board.clear()
    game_board.fill_cells([s.head], util.Color(220, 0, 0))
    for i in range(1, len(s.body)):
        game_board.fill_cells([s.body[i]], util.Color(200 - i * (100 // len(s.body)), 0, 0))
    #game_board.fill_cells(s.body[1:], util.Color(100, 0, 0))
    game_board.fill_cells([food], util.Color(0, 100, 0))
    game_board.draw()

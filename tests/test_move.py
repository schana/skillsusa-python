import pytest
import itertools

from game import runner
from game import main
from game import util
from game import snake


def games():
    for length in range(3):
        rows = length + 2
        columns = length + 2
        for sr, sc, fr, fc in itertools.product(range(rows), range(columns), repeat=2):
            for body in generate_bodies(util.Cell(sr, sc), length, rows, columns):
                s = snake.Snake('star', body[0], lambda p: main.call_move(p, main.star_snake))
                g = runner.Game(rows=rows, columns=columns, display=False)
                s.body = body
                g.snakes = [s]
                g.food = util.Cell(fr, fc)
                yield g


def generate_bodies(head, length, rows, columns):
    return get_all([head], length - 1, rows, columns)


def get_all(body, length, rows, columns):
    if length == 0:
        yield body
    else:
        for b in growth_possibilities(body, rows, columns):
            yield from get_all(b, length - 1, rows, columns)


def growth_possibilities(body, rows, columns):
    for n in get_neighbors(body[-1], body, rows, columns):
        new_body = body.copy()
        new_body.append(n)
        yield new_body


def get_neighbors(a: util.Cell, taken, rows, columns):
    up = util.Cell(a.r - 1, a.c)
    right = util.Cell(a.r, a.c + 1)
    down = util.Cell(a.r + 1, a.c)
    left = util.Cell(a.r, a.c - 1)
    for c in up, right, down, left:
        if is_valid_cell(c, taken, rows, columns):
            yield c


def is_valid_cell(cell, taken, rows, columns):
    return 0 <= cell.r < rows and 0 <= cell.c < columns and cell not in taken


@pytest.mark.parametrize('game', games())
def test_snake(game):
    for moves in range(2):
        game.move_snake(game.snakes[0])
        assert game.snakes[0].alive

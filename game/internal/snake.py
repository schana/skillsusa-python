from game import cell
from game.internal import body

mover = None
alive = None
consumed_food = False


def move(food):
    global consumed_food, alive
    d = mover.get_next_direction()
    next_head = cell.get_neighbor(body.get_head(), d)
    consumed_food = next_head == food
    body.move(next_head, consumed_food)
    alive = alive and body.is_valid()

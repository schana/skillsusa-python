from game import board
from game import direction


class BlindMover:
    def get_next_direction(self):
        head = board.get_head()
        food = board.get_food()
        if head.row > food.row:
            return direction.UP
        elif head.row < food.row:
            return direction.DOWN
        elif head.column > food.column:
            return direction.LEFT
        else:
            return direction.RIGHT


def completionist_snake(head, body, food, board_width, board_height):
    if head.r == board_height - 1:
        if head.c % 2 == 0:
            return 'r'
        else:
            return 'u'
    else:
        if head.r == 0:
            if head.c == 0:
                return 'd'
            else:
                return 'l'
        elif head.r == 1:
            if head.c == board_width - 1:
                return 'u'
            else:
                if head.c % 2 == 0:
                    return 'd'
                else:
                    return 'r'
        else:
            if head.c % 2 == 0:
                return 'd'
            else:
                return 'u'

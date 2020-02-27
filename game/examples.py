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


class CompletionistMover:
    def get_next_direction(self):
        head = board.get_head()
        if head.row == board.ROWS - 1:
            if head.column % 2 == 0:
                return direction.RIGHT
            else:
                return direction.UP
        else:
            if head.row == 0:
                if head.column == 0:
                    return direction.DOWN
                else:
                    return direction.LEFT
            elif head.row == 1:
                if head.column == board.COLUMNS - 1:
                    return direction.UP
                else:
                    if head.column % 2 == 0:
                        return direction.DOWN
                    else:
                        return direction.RIGHT
            else:
                if head.column % 2 == 0:
                    return direction.DOWN
                else:
                    return direction.UP

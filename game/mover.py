from game import direction
from game import board


class SnakeMover:
    """
    This is the base mover that you'll be extending. It informs the game how
    your snake should move. Everything about the board's state can be accessed
    from the 'board' module that's imported above. Look in board.py or check
    the examples for usages.
    """

    def get_next_direction(self):
        """
        :return: the next direction for your snake to move
        """
        return direction.UP

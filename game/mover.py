from game import direction


class SnakeMover:
    """
    This is the base mover that you'll be extending. It informs the game how
    your snake should move.
    """
    def __init__(self, board):
        """

        :param board: board the game board that holds the state of the snake's
                      body, food location, and the size of the board
        """
        self.board = board

    def get_next_direction(self):
        """
        :return: the next direction for your snake to move
        """
        return direction.UP

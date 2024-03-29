"""
This holds the current game state. The board is in a grid shape with 0-based
row and column indices represented by (row, column) Cells:

(0, 0), (0, 1), (0, 2), ..., (0, COLUMNS - 1)
(1, 0), (1, 1), (1, 2), ..., (1, COLUMNS - 1)
...
(ROWS - 1, 0), (ROWS - 1, 1), ..., (ROWS - 1, COLUMNS - 1)
"""

ROWS = 10
COLUMNS = 10
body = []
food = None


def get_head():
    """
    :return: the cell representing the head of the snake
    """
    return body[0]


def get_body():
    """
    :return: the list of cells making up the snake, including the head
    """
    return body


def get_food():
    """
    :return: the Cell representing the location of the food
    """
    return food

from collections import namedtuple

from game import direction

Cell = namedtuple('Cell', 'row, column')


def get_neighbor(cell, neighbor_direction):
    """
    Gets a Cell's neighbor in the specified direction. Note that this does
    not perform any boundary checking and could return invalid cells

    :param cell: the cell to get the neighbor of
    :param neighbor_direction: the direction of the neighbor
    :return: the neighbor cell in the specified direction
    """
    if neighbor_direction == direction.UP:
        return get_up(cell)
    elif neighbor_direction == direction.DOWN:
        return get_down(cell)
    elif neighbor_direction == direction.LEFT:
        return get_left(cell)
    elif neighbor_direction == direction.RIGHT:
        return get_right(cell)
    return None


def get_left(cell):
    return Cell(cell.row, cell.column - 1)


def get_right(cell):
    return Cell(cell.row, cell.column + 1)


def get_up(cell):
    return Cell(cell.row - 1, cell.column)


def get_down(cell):
    return Cell(cell.row + 1, cell.column)

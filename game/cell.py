from game import direction


class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def get_neighbor(self, neighbor_direction):
        """
        Gets a Cell's neighbor in the specified direction. Note that this does
        not perform any boundary checking and could return invalid cells

        :param neighbor_direction: the direction of the neighbor
        :return: the neighbor cell in the specified direction
        """
        if neighbor_direction == direction.UP:
            return self.get_up()
        elif neighbor_direction == direction.DOWN:
            return self.get_down()
        elif neighbor_direction == direction.LEFT:
            return self.get_left()
        elif neighbor_direction == direction.RIGHT:
            return self.get_right()
        return None

    def get_left(self):
        return Cell(self.row, self.column - 1)

    def get_right(self):
        return Cell(self.row, self.column + 1)

    def get_up(self):
        return Cell(self.row - 1, self.column)

    def get_down(self):
        return Cell(self.row + 1, self.column)

    def __str__(self):
        return '({}, {})'.format(self.row, self.column)

    def __eq__(self, other):
        """
        Determines equality based on hash
        :param other: object to compare to
        :return: whether hashes match
        """
        if isinstance(other, Cell):
            return hash(self) == hash(other)
        return False

    def __hash__(self):
        """
        Hash calculated based on offset column and row, such that two cells with
        equal rows and columns will have the same hash code
        :return: simple hash based on row and column
        """
        return self.row + self.column * 10000

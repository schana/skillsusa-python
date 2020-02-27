from game import board


class Body:
    def __init__(self, head):
        self.cells = [head]

    def move(self, next_head, should_grow):
        self.cells.insert(0, next_head)
        if not should_grow:
            self.cells.pop()

    def is_valid(self):
        # Check for overlaps
        if len(set(self.cells)) != len(self.cells):
            return False
        # Check boundaries
        for cell in self.cells:
            if not self.is_body_part_valid(cell):
                return False
        return True

    def is_body_part_valid(self, cell):
        if cell.row < 0 or cell.row >= board.ROWS:
            return False
        if cell.column < 0 or cell.column >= board.COLUMNS:
            return False
        return True

    def get_head(self):
        return self.cells[0]

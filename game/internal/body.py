from game import board

cells = []


def initialize(head):
    global cells
    cells = [head]


def move(next_head, should_grow):
    cells.insert(0, next_head)
    if not should_grow:
        cells.pop()


def is_valid():
    # Check for overlaps
    if len(set(cells)) != len(cells):
        return False
    # Check boundaries
    for cell in cells:
        if cell.row < 0:
            return False
        if cell.row >= board.ROWS:
            return False
        if cell.column < 0:
            return False
        if cell.column >= board.COLUMNS:
            return False
    return True


def get_head():
    return cells[0]

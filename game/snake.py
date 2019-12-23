import typing

from game import util
Cell = typing.NewType('Cell', util.Cell)


class Snake:
    def __init__(self, head: Cell):
        self.head = head
        self.body = [self.head]

    def do_move(self, direction):
        if direction == 'u':
            new_head = util.Cell(self.head.r - 1, self.head.c)
        elif direction == 'd':
            new_head = util.Cell(self.head.r + 1, self.head.c)
        elif direction == 'l':
            new_head = util.Cell(self.head.r, self.head.c - 1)
        else:
            new_head = util.Cell(self.head.r, self.head.c + 1)
        self.head = new_head
        self.body.insert(0, self.head)

    def should_die(self, last_cell: Cell, should_grow=False):
        if not should_grow:
            del self.body[-1]
        if len(self.body) != len(set(self.body)):
            return True
        if self.head.r < 0 or self.head.c < 0 or self.head.r > last_cell.r or self.head.c > last_cell.c:
            return True
        return False

    def move(self, food, board_width=None, board_height=None):
        from math import sqrt, pow

        def heuristic_cost_estimate(start, goal):
            return sqrt(pow(abs(start.c-goal.c), 2) + pow(abs(start.r-goal.r), 2))

        def get_direct_neighbours(point):
            return [
                util.Cell(c=point.c+1, r=point.r),
                util.Cell(c=point.c-1, r=point.r),
                util.Cell(c=point.c, r=point.r+1),
                util.Cell(c=point.c, r=point.r-1)
                ]

        def neighbour_nodes(point):
            neighbours = []
            for new_point in get_direct_neighbours(point):
                if new_point in self.body or 0 > new_point.c >= board_width-1 or 0 > new_point.r >= board_height-1:
                    continue
                neighbours.append(new_point)
            return neighbours

        def reconstruct_path(came_from, current_node):
            if current_node in came_from:
                p = reconstruct_path(came_from, came_from[current_node])
                p.append(current_node)
                return p
            else:
                return [current_node]

        def get_direction(point1, point2):
            if point2.c == point1.c+1 and point2.r == point1.r:
                return 'r'
            elif point2.c == point1.c-1 and point2.r == point1.r:
                return 'l'
            elif point2.c == point1.c and point2.r == point1.r+1:
                return 'd'
            elif point2.c == point1.c and point2.r == point1.r-1:
                return 'u'
            return 'u'

        start = self.head
        if len(self.body) < 30:
            goal = food
        else:
            r, c = 0, 0
            if self.head.r == board_height - 1:
                if self.head.c % 2 == 0:
                    r = self.head.r
                    c = self.head.c + 1
                else:
                    r = self.head.r - 1
                    c = self.head.c
            else:
                if self.head.r == 0:
                    if self.head.c == 0:
                        r = self.head.r + 1
                        c = self.head.c
                    else:
                        r = self.head.r
                        c = self.head.c - 1
                elif self.head.r == 1:
                    if self.head.c == board_width - 1:
                        r = self.head.r - 1
                        c = self.head.c
                    else:
                        if self.head.c % 2 == 0:
                            r = self.head.r + 1
                            c = self.head.c
                        else:
                            r = self.head.r
                            c = self.head.c + 1
                else:
                    if self.head.c % 2 == 0:
                        r = self.head.r + 1
                    else:
                        r = self.head.r - 1
                    c = self.head.c
            goal = util.Cell(r, c)
        closedset = []
        openset = [start]
        came_from = {}

        g_score = {start: 0}
        f_score = {start: g_score[start] + heuristic_cost_estimate(start, goal)}

        possibility_counter = 0
        while openset:
            possibility_counter += 1
            if possibility_counter > 500:
                break
            current = min(openset, key=lambda x: f_score.get(x))
            if current == goal:
                path = reconstruct_path(came_from, goal)
                if len(path) > 0:
                    next_point = path[min(len(path)-1, 1)]
                else:
                    return 'r'
                direction = get_direction(start, next_point)
                return direction

            openset.remove(current)
            closedset.append(current)

            for neighbour in neighbour_nodes(current):
                if neighbour in closedset:
                    continue
                tentative_g_score = g_score[current] + 1

                if neighbour not in openset or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = g_score[neighbour] + heuristic_cost_estimate(neighbour, goal)
                    if neighbour not in openset:
                        openset.append(neighbour)
        for point in get_direct_neighbours(self.head):
            if point in self.body or 0 >= point.c > board_width-1 or 0 >= point.r > board_height-1:
                continue
            return get_direction(self.head, point)
        return 'u'

'''
    def move(self, food: Cell):
        if self.head.r > food.r:
            return 'u'
        elif self.head.r < food.r:
            return 'd'
        elif self.head.c > food.c:
            return 'l'
        else:
            return 'r'
'''
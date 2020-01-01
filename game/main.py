from game import runner
import json
from game import util
import random


def main():
    g = runner.Game(10, 10, display=False)
    g.add_snake('alice', lambda p: call_move(p, move1))
    g.add_snake('bob', lambda p: call_move(p, move2))
    g.add_snake('charlie', lambda p: call_move(p, move3))
    g.run()
    scores = g.get_scores()
    for i in range(1000):
        print(i)
        g.snakes = []
        g.add_snake('alice', lambda p: call_move(p, move1))
        g.add_snake('bob', lambda p: call_move(p, move2))
        g.add_snake('charlie', lambda p: call_move(p, move3))
        g.run()
        new_scores = g.get_scores()
        for n in ['alice', 'bob', 'charlie']:
            for j in ['score', 'age']:
                scores[n][j] += new_scores[n][j]
    print(json.dumps(scores, indent=2))


def unpack(parameters):
    params = json.loads(parameters)
    params['head'] = util.Cell(r=params['head']['r'], c=params['head']['c'])
    params['body'] = [util.Cell(r=p['r'], c=p['c']) for p in params['body']]
    params['filled'] = [util.Cell(r=p['r'], c=p['c']) for p in params['filled']]
    params['food'] = util.Cell(r=params['food']['r'], c=params['food']['c'])
    return params


def call_move(json_parameters, move_fun):
    params = unpack(json_parameters)
    return move_fun(params['head'], params['body'], params['filled'], params['food'], params['columns'], params['rows'])


def move1(*args):
    return random.choice(['l', 'r', 'u', 'd'])


def move2(head, body, filled, food, columns, rows):
    if head.r > food.r:
        return 'u'
    elif head.r < food.r:
        return 'd'
    elif head.c > food.c:
        return 'l'
    else:
        return 'r'


def move3(head, body, filled_cells, food, board_width, board_height):
    if filled_cells is None:
        filled_cells = []
    from math import sqrt, pow

    def heuristic_cost_estimate(start, goal):
        return sqrt(pow(abs(start.c - goal.c), 2) + pow(abs(start.r - goal.r), 2))

    def get_direct_neighbours(point):
        return [
            util.Cell(c=point.c + 1, r=point.r),
            util.Cell(c=point.c - 1, r=point.r),
            util.Cell(c=point.c, r=point.r + 1),
            util.Cell(c=point.c, r=point.r - 1)
        ]

    def neighbour_nodes(point):
        neighbours = []
        for new_point in get_direct_neighbours(point):
            if new_point in body or new_point in filled_cells or 0 > new_point.c >= board_width - 1 or 0 > new_point.r >= board_height - 1:
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
        if point2.c == point1.c + 1 and point2.r == point1.r:
            return 'r'
        elif point2.c == point1.c - 1 and point2.r == point1.r:
            return 'l'
        elif point2.c == point1.c and point2.r == point1.r + 1:
            return 'd'
        elif point2.c == point1.c and point2.r == point1.r - 1:
            return 'u'
        return 'u'

    start = head
    if len(body) < 300:
        goal = food
    else:
        r, c = 0, 0
        if head.r == board_height - 1:
            if head.c % 2 == 0:
                r = head.r
                c = head.c + 1
            else:
                r = head.r - 1
                c = head.c
        else:
            if head.r == 0:
                if head.c == 0:
                    r = head.r + 1
                    c = head.c
                else:
                    r = head.r
                    c = head.c - 1
            elif head.r == 1:
                if head.c == board_width - 1:
                    r = head.r - 1
                    c = head.c
                else:
                    if head.c % 2 == 0:
                        r = head.r + 1
                        c = head.c
                    else:
                        r = head.r
                        c = head.c + 1
            else:
                if head.c % 2 == 0:
                    r = head.r + 1
                else:
                    r = head.r - 1
                c = head.c
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
                next_point = path[min(len(path) - 1, 1)]
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
    for point in get_direct_neighbours(head):
        if point in body or point in filled_cells or 0 >= point.c > board_width - 1 or 0 >= point.r > board_height - 1:
            continue
        return get_direction(head, point)
    return 'u'


if __name__ == '__main__':
    main()

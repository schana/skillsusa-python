from game import runner
import json
from game import util
import random

RUNS = 1
DISPLAY = False
RECORD = False
DELAY = 20
TURN_LIMIT = 1000


def main():
    g = runner.Game(40, 40, turn_limit=TURN_LIMIT, display=DISPLAY, record=RECORD, delay=DELAY)
    scores = {}
    for i in range(RUNS):
        print(i)
        g.snakes = []
        g.add_snake('alice', lambda p: call_move(p, blind_snake))
        g.add_snake('bob', lambda p: call_move(p, random_snake))
        g.add_snake('charlie', lambda p: call_move(p, star_snake))
        g.add_snake('david', lambda p: call_move(p, brute_force_snake))
        g.run(i)
        if RECORD:
            animate_game(i)
        new_scores = g.get_scores()
        for n in ['alice', 'bob', 'charlie', 'david']:
            snake_score = scores.get(n, {})
            scores[n] = snake_score
            for j in ['score', 'age']:
                scores[n][j] = scores[n].get(j, 0) + new_scores.get(n, {}).get(j, 0)
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


def random_snake(*args):
    return random.choice(['l', 'r', 'u', 'd'])


def blind_snake(head, body, filled, food, columns, rows):
    if head.r > food.r:
        return 'u'
    elif head.r < food.r:
        return 'd'
    elif head.c > food.c:
        return 'l'
    else:
        return 'r'


def star_snake(head, body, filled_cells, food, board_width, board_height):
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
    goal = food
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


def brute_force_snake(head, body, filled_cells, food, board_width, board_height):
    if head.r == board_height - 1:
        if head.c % 2 == 0:
            return 'r'
        else:
            return 'u'
    else:
        if head.r == 0:
            if head.c == 0:
                return 'd'
            else:
                return 'l'
        elif head.r == 1:
            if head.c == board_width - 1:
                return 'u'
            else:
                if head.c % 2 == 0:
                    return 'd'
                else:
                    return 'r'
        else:
            if head.c % 2 == 0:
                return 'd'
            else:
                return 'u'


def animate_game(identifier):
    import subprocess, os

    files = []

    for root, dirs, fs in os.walk('pics'):
        for f in fs:
            files.append(str(root) + '/' + str(f))

    command = [
        'C:/Program Files/ImageMagick-7.0.9-Q16/magick.exe',
        'convert',
        '-delay', '5',
        '-size', '545x545'
    ] + files + [
        'anim_' + str(identifier) + '.gif'
    ]

    subprocess.call(command)


if __name__ == '__main__':
    main()

def blind_snake(head, body, food, columns, rows):
    if head.r > food.r:
        return 'u'
    elif head.r < food.r:
        return 'd'
    elif head.c > food.c:
        return 'l'
    else:
        return 'r'


def completionist_snake(head, body, food, board_width, board_height):
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
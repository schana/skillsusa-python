from game import board
from game.internal import game_state

RUNS = 1000000
DISPLAY = False
RECORD = False
DELAY = 50
TURN_LIMIT = 1000
runs = 0


def main():
    global runs
    g = game_state.GameState(board.Board())
    if DISPLAY:
        # do graphics stuff
        pass
    else:
        sum_score = 0
        sum_age = 0
        while runs < RUNS:
            if g.snake.alive and g.age < TURN_LIMIT:
                g.step()
            else:
                runs += 1
                sum_score += g.get_score()
                sum_age += g.age
                g.reset()
                if runs % (RUNS / 20) == 0:
                    print('{}% complete'.format(100 * runs / RUNS))
        print('Average Score: ', float(sum_score) / runs, ', Average Age: ', float(sum_age) / runs, sep='')

'''
        if RECORD:
            animate_game(i)
'''

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

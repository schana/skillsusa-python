from game.internal import game_state
from game.internal import snake

RUNS = 100000
DISPLAY = False
RECORD = False
DELAY = 50
TURN_LIMIT = 1000
runs = 0


def main():
    global runs
    game_state.reset()
    if DISPLAY:
        # do graphics stuff
        pass
    else:
        sum_score = 0
        sum_age = 0
        while runs < RUNS:
            if snake.alive and game_state.age < TURN_LIMIT:
                game_state.step()
            else:
                runs += 1
                sum_score += game_state.get_score()
                sum_age += game_state.age
                game_state.reset()
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

from game import config
from game.internal import game_state, graphics
from game.internal import snake

RECORD = False
TURN_LIMIT = 1000
runs = 0


def main():
    global runs
    game_state.reset()
    if config.DISPLAY:
        painter = graphics.Painter()
        painter.initialize()
        while True:
            painter.clear()
            painter.draw_boarders()
            painter.draw_snake()
            painter.draw_food()
            if snake.alive and game_state.age < TURN_LIMIT:
                painter.draw(delay=config.DELAY)
                game_state.step()
            else:
                painter.draw(delay=1000)
                runs += 1
                print(runs, 'Score:', game_state.get_score(), 'Age:', game_state.age)
                game_state.reset()
    else:
        sum_score = 0
        sum_age = 0
        while runs < config.RUNS:
            if snake.alive and game_state.age < TURN_LIMIT:
                game_state.step()
            else:
                runs += 1
                sum_score += game_state.get_score()
                sum_age += game_state.age
                game_state.reset()
                if runs % (config.RUNS / 20) == 0:
                    print('{}% complete'.format(100 * runs / config.RUNS))
        print('Average Score: ', float(sum_score) / runs, ', Average Age: ', float(sum_age) / runs, sep='')


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

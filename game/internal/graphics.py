import sys

import pygame

from game import board
from game.internal import body, game_state
from game.internal import snake

CELL_SIZE = 40
PADDING = 5
COLOR_BACKGROUND = (0, 0, 0)
COLOR_BORDER = (100, 100, 100)
COLOR_SNAKE = (180, 180, 180)
COLOR_INVALID = (240, 50, 50)
COLOR_FOOD = (0, 100, 0)


class Painter:
    screen = None
    i = 0

    def __init__(self, record=False):
        self.record = record

    def get_height(self):
        return (2 + board.ROWS) * CELL_SIZE + board.ROWS * PADDING

    def get_width(self):
        return (2 + board.COLUMNS) * CELL_SIZE + board.COLUMNS * PADDING

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.get_width(), self.get_height()))
        pygame.display.set_caption('Snake')

    def draw_food(self):
        surface = pygame.Surface((CELL_SIZE - PADDING, CELL_SIZE - PADDING))
        surface.fill(COLOR_FOOD)
        rect = surface.get_rect(top=CELL_SIZE + PADDING + game_state.food.row * (CELL_SIZE + PADDING),
                                left=CELL_SIZE + PADDING + game_state.food.column * (CELL_SIZE + PADDING))
        self.screen.blit(surface, rect)

    def draw_snake(self):
        surface = pygame.Surface((CELL_SIZE - PADDING, CELL_SIZE - PADDING))
        fill_horizontal = pygame.Surface((PADDING * 2, CELL_SIZE - PADDING))
        fill_vertical = pygame.Surface((CELL_SIZE - PADDING, PADDING * 2))
        surface.fill(COLOR_SNAKE)
        fill_horizontal.fill(COLOR_SNAKE)
        fill_vertical.fill(COLOR_SNAKE)
        previous = None
        for cell in body.cells:
            rect = surface.get_rect(
                top=CELL_SIZE + PADDING + cell.row * (CELL_SIZE + PADDING),
                left=CELL_SIZE + PADDING + cell.column * (CELL_SIZE + PADDING))
            self.screen.blit(surface, rect)
            if previous is not None:
                dr, dc = cell.row - previous.row, cell.column - previous.column
                if dr == 0:
                    if dc == -1:
                        rect = fill_horizontal.get_rect(
                            top=CELL_SIZE + cell.row * (CELL_SIZE + PADDING) + PADDING,
                            left=CELL_SIZE + previous.column * (CELL_SIZE + PADDING) - PADDING)
                    else:
                        rect = fill_horizontal.get_rect(
                            top=CELL_SIZE + cell.row * (CELL_SIZE + PADDING) + PADDING,
                            left=CELL_SIZE + cell.column * (CELL_SIZE + PADDING) - PADDING)
                    self.screen.blit(fill_horizontal, rect)
                else:
                    if dr == -1:
                        rect = fill_vertical.get_rect(
                            top=CELL_SIZE + previous.row * (CELL_SIZE + PADDING) - PADDING,
                            left=CELL_SIZE + cell.column * (CELL_SIZE + PADDING) + PADDING)
                    else:
                        rect = fill_vertical.get_rect(
                            top=CELL_SIZE + cell.row * (CELL_SIZE + PADDING) - PADDING,
                            left=CELL_SIZE + cell.column * (CELL_SIZE + PADDING) + PADDING)
                    self.screen.blit(fill_vertical, rect)
            previous = cell
        if not snake.alive:
            surface.fill(COLOR_INVALID)
            rect = surface.get_rect(top=CELL_SIZE + PADDING + body.get_head().row * (CELL_SIZE + PADDING),
                                    left=CELL_SIZE + PADDING + body.get_head().column * (CELL_SIZE + PADDING))
            self.screen.blit(surface, rect)

    def clear(self):
        self.screen.fill(COLOR_BACKGROUND)

    def draw_boarders(self):
        # top
        pygame.draw.rect(self.screen, COLOR_BORDER,
                         [0, 0, self.get_width(), CELL_SIZE - PADDING])
        # bottom
        pygame.draw.rect(self.screen, COLOR_BORDER,
                         [0, self.get_height() - CELL_SIZE + PADDING, self.get_width(), self.get_height()])
        # left
        pygame.draw.rect(self.screen, COLOR_BORDER,
                         [0, CELL_SIZE - PADDING, CELL_SIZE - PADDING, self.get_height()])
        # right
        pygame.draw.rect(self.screen, COLOR_BORDER,
                         [self.get_width() - CELL_SIZE + PADDING, 0, self.get_width(), self.get_height()])

    def draw(self, identifier=0, record=False, delay=50):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        if record:
            pygame.image.save(self.screen, 'pics/pic_' + str(identifier) + '_' + str(self.i) + '.png')
        self.i += 1
        pygame.time.delay(delay)

import itertools
import sys

import pygame

from game import cell


class Painter:
    screen = None
    i = 0

    def __init__(self, rows=10, columns=10, cell_size=20, padding=2, display=False, record=False):
        self.rows = rows
        self.columns = columns
        self.cells = {cell.Cell(r, c) for r, c in itertools.product(range(self.rows), range(self.columns))}
        self.cell_size = cell_size
        self.padding = padding
        self.display = display
        self.record = record

    def get_height(self):
        return (2 + self.rows) * self.cell_size + self.rows * self.padding

    def get_width(self):
        return (2 + self.columns) * self.cell_size + self.columns * self.padding

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.get_width(), self.get_height()))

    def fill_cells(self, cells, color):
            surface = pygame.Surface((self.cell_size - self.padding, self.cell_size - self.padding))
            fill_horizontal = pygame.Surface((self.padding * 2, self.cell_size - self.padding))
            fill_vertical = pygame.Surface((self.cell_size - self.padding, self.padding * 2))
            surface.fill(color)
            fill_horizontal.fill(color)
            fill_vertical.fill(color)
            previous = None
            for cell in cells:
                rect = surface.get_rect(
                    top=self.cell_size + self.padding + cell.r * (self.cell_size + self.padding),
                    left=self.cell_size + self.padding + cell.c * (self.cell_size + self.padding))
                self.screen.blit(surface, rect)
                if previous is not None:
                    dr, dc = cell.r - previous.r, cell.c - previous.c
                    if dr == 0:
                        if dc == -1:
                            rect = fill_horizontal.get_rect(top=self.cell_size +cell.r * (self.cell_size + self.padding) + self.padding,
                                                            left=self.cell_size +previous.c * (self.cell_size + self.padding) - self.padding)
                        else:
                            rect = fill_horizontal.get_rect(top=self.cell_size +cell.r * (self.cell_size + self.padding) + self.padding,
                                                            left=self.cell_size +cell.c * (self.cell_size + self.padding) - self.padding)
                        self.screen.blit(fill_horizontal, rect)
                    else:
                        if dr == -1:
                            rect = fill_vertical.get_rect(top=self.cell_size +previous.r * (self.cell_size + self.padding) - self.padding,
                                                          left=self.cell_size +cell.c * (self.cell_size + self.padding) + self.padding)
                        else:
                            rect = fill_vertical.get_rect(top=self.cell_size +cell.r * (self.cell_size + self.padding) - self.padding,
                                                          left=self.cell_size +cell.c * (self.cell_size + self.padding) + self.padding)
                        self.screen.blit(fill_vertical, rect)
                previous = cell

    def clear(self, color=(0, 0, 0)):
        self.screen.fill(color)
        # top
        pygame.draw.rect(self.screen, (100, 100, 100),
                         [0, 0, self.get_width(), self.cell_size - self.padding])
        # bottom
        pygame.draw.rect(self.screen, (100, 100, 100),
                         [0, self.get_height() - self.cell_size + self.padding, self.get_width(), self.get_height()])
        # left
        pygame.draw.rect(self.screen, (100, 100, 100),
                         [0, self.cell_size - self.padding, self.cell_size - self.padding, self.get_height()])
        # right
        pygame.draw.rect(self.screen, (100, 100, 100),
                         [self.get_width() - self.cell_size + self.padding, 0, self.get_width(), self.get_height()])

    def draw(self, identifier=0, record=False, delay=50):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        if record:
            pygame.image.save(self.screen, 'pics/pic_' + str(identifier) + '_' + str(self.i) + '.png')
        self.i += 1
        pygame.time.delay(delay)

import random
import sys
import typing

import pygame

from game import util
Cells = typing.List[util.Cell]
Color = typing.NewType('Color', util.Color)


class Board:
    screen = None

    def __init__(self, rows=16, columns=20, cell_size=50, padding=5):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size
        self.padding = padding

    def get_height(self):
        return self.rows * self.cell_size + (self.rows - 1) * self.padding

    def get_width(self):
        return self.columns * self.cell_size + (self.columns - 1) * self.padding

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.get_width(), self.get_height()))

    def fill_cells(self, cells: Cells, color):
        surface = pygame.Surface((self.cell_size, self.cell_size))
        surface.fill(color)
        for cell in cells:
            rect = surface.get_rect(
                top=cell.r*(self.cell_size + self.padding), left=cell.c*(self.cell_size + self.padding))
            self.screen.blit(surface, rect)

    def clear(self, color: Color = util.Color(0, 0, 0)):
        self.screen.fill(color)

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(50)

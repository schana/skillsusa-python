import itertools
import sys
import typing
import time
import os

import pygame

from game import util
Cells = typing.List[util.Cell]
Color = typing.NewType('Color', util.Color)


class Board:
    screen = None
    i = 0

    def __init__(self, rows=16, columns=20, cell_size=50, padding=5, gui=False):
        self.rows = rows
        self.columns = columns
        self.cells = {util.Cell(r, c) for r, c in itertools.product(range(self.rows), range(self.columns))}
        self.cell_size = cell_size
        self.padding = padding
        self.gui = gui

    def get_height(self):
        return self.rows * self.cell_size + (self.rows - 1) * self.padding

    def get_width(self):
        return self.columns * self.cell_size + (self.columns - 1) * self.padding

    def initialize(self):
        if self.gui:
            pygame.init()
            self.screen = pygame.display.set_mode((self.get_width(), self.get_height()))
        else:
            row = [' '] * self.columns
            self.screen = [row.copy() for i in range(self.rows)]

    def fill_cells(self, cells: Cells, color, letter='x'):
        if self.gui:
            surface = pygame.Surface((self.cell_size, self.cell_size))
            surface.fill(color)
            for cell in cells:
                rect = surface.get_rect(
                    top=cell.r*(self.cell_size + self.padding), left=cell.c*(self.cell_size + self.padding))
                self.screen.blit(surface, rect)
        else:
            for cell in cells:
                self.screen[cell.r][cell.c] = letter

    def clear(self, color: Color = util.Color(0, 0, 0)):
        if self.gui:
            self.screen.fill(color)

    def draw(self, identifier=0, record=False, delay=50):
        if self.gui:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            if record:
                pygame.image.save(self.screen, 'pics/pic_' + str(identifier) + '_' + str(self.i) + '.png')
            self.i += 1
            pygame.time.delay(delay)
        else:
            new_board = ''.join(('+-', '-' * 2 * self.columns, '+'))
            new_board += '\n'
            for r in self.screen:
                new_board += '| '
                for c in r:
                    new_board += c + ' '
                new_board += '|\n'
            new_board += ''.join(('+-', '-' * 2 * self.columns, '+'))
            new_board += '\n'
            os.system('cls')
            print(new_board)
            row = [' '] * self.columns
            self.screen = [row.copy() for i in range(self.rows)]
            time.sleep(delay / 1000)

#  ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import pygame
import chess
from _constants import *


class Board:
    location = (50, 50)
    sqSize = 100
    
    def __init__(self):
        self.board = chess.Board()

    def Draw(self, window):
        self.DrawSquares(window)
        self.DrawPieces(window)

    def DrawSquares(self, window):
        for row in range(8):
            for col in range(8):
                loc = (self.sqSize*col + self.location[0], self.sqSize*row + self.location[1])
                color = BOARD_WHITE if (row+col) % 2 == 0 else BOARD_BLACK
                pygame.draw.rect(window, color, loc+(self.sqSize, self.sqSize))

    def DrawPieces(self, window):
        for row in range(8):
            for col in range(8):
                index = 8*(7-row) + col
                piece = self.board.piece_at(index)
                if piece is not None:
                    symbol = piece.symbol()
                    if symbol.islower():
                        symbol = "b" + symbol
                    elif symbol.isupper():
                        symbol = "w" + symbol.lower()

                    img = IMAGES[symbol]
                    loc = (self.sqSize*col + self.location[0] + 5, self.sqSize*row + self.location[1] + 5)
                    window.blit(img, loc)
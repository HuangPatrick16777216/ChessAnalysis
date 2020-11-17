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
import threading
import chess
import chess.pgn
import chess.engine
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from pumpkinpy.pygameutils.elements import ButtonText, TextInput
from _constants import *
Tk().withdraw()

class Buttons:
    buttonLoadPgn = ButtonText((900, 50), (200, 50), WHITE, CYAN, BLACK, FONT_SMALL.render("Load PGN", 1, BLACK), border=3, borderCol=WHITE)
    buttonLoadEngine = ButtonText((900, 200), (200, 50), WHITE, CYAN, BLACK, FONT_SMALL.render("Load Engine", 1, BLACK), border=3, borderCol=WHITE)
    inputAnalysisDepth = TextInput((900, 350), (200, 50), WHITE, 3, WHITE, label="Depth", font=FONT_SMALL)
    buttonAnalyse = ButtonText((900, 500), (200, 50), WHITE, CYAN, BLACK, FONT_SMALL.render("Analyse", 1, BLACK), border=3, borderCol=WHITE)

    pgnPath = ""
    enginePath = ""
    analysing = False

    def Draw(self, window, events, board):
        if self.analysing:
            progress = board.analyseCurrMove / len(board.moves)
            self.analysing = board.analysing
            
            pygame.draw.rect(window, CYAN, (900, 100, 500*progress, 50))
            pygame.draw.rect(window, WHITE, (900, 100, 500, 50), 2)
            return

        self.buttonLoadPgn.Draw(window, events)
        self.buttonLoadEngine.Draw(window, events)
        self.inputAnalysisDepth.Draw(window, events)
        self.buttonAnalyse.Draw(window, events)

        pgnText = FONT_SMALL.render(self.pgnPath, 1, WHITE)
        engineText = FONT_SMALL.render(self.enginePath, 1, WHITE)
        window.blit(pgnText, (900, 125))
        window.blit(engineText, (900, 275))

        if self.buttonLoadPgn.clicked:
            self.pgnPath = askopenfilename()
            board.LoadPgn(self.pgnPath)
        if self.buttonLoadEngine.clicked:
            self.enginePath = askopenfilename()
        if self.buttonAnalyse.clicked:
            self.analysing = True
            threading.Thread(target=board.Analyse, args=(self.enginePath, int(self.inputAnalysisDepth.text))).start()


class Board:
    location = (50, 50)
    sqSize = 100
    
    def __init__(self):
        self.board = chess.Board()
        self.moves = []
        self.currMove = 0
        self.analyseCurrMove = 0
        self.analysing = False

    def LoadPgn(self, path):
        if path == "":
            return

        with open(path, "r") as file:
            game = chess.pgn.read_game(file)
            self.moves = list(game.mainline_moves())

    def UpdateBoard(self):
        self.board = chess.Board()
        for move in self.moves[:self.currMove]:
            self.board.push(move)

    def Draw(self, window, events):
        self.DrawSquares(window)
        self.DrawPieces(window)
        self.Update(events)

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

    def Update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.currMove = max(self.currMove-1, 0)
                    self.UpdateBoard()
                elif event.key == pygame.K_RIGHT:
                    self.currMove = min(self.currMove+1, len(self.moves))
                    self.UpdateBoard()

    def Analyse(self, enginePath, depth):
        if enginePath == "":
            return

        self.analysing = True
        self.analyseCurrMove = 0
        engine = chess.engine.SimpleEngine.popen_uci(enginePath)
        board = chess.Board()
        self.evals = [0]
        for i, move in enumerate(self.moves):
            board.push(move)
            self.analyseCurrMove = i + 1
            score = engine.analyse(board, chess.engine.Limit(depth=depth))["score"].pov(chess.WHITE)
            self.evals.append(score)
        self.analysing = False
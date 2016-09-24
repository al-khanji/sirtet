# Copyright (C) 2008 Louai "slougi" Al-Khanji <louai.khanji@gmail.com>

# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely without any restrictions.

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from game import Game
from view import GameView, NextBlockView, ScoreView, LevelView

# game grid size
WIDTH = 10
HEIGHT = 22

# update interval (ms)
INTERVAL = 20

# initial step time (ms)
STEP_TIME = 1500

# increase difficulty level after this many ticks
TICK_INCREASE = 200

# blocks are described as a list of (x, y) tuples. the coordinates describe
# occupied brick positions relative to a top-left origin
BLOCKS = [
    [( 0,-1), ( 0, 0), ( 0, 1), ( 0, 2)], # |
    [( 0, 0), ( 1, 1), ( 1, 0), ( 0, 1)], # square
    [(-1,-1), (-1, 0), ( 0, 0), ( 0, 1)], # s
    [( 0,-1), ( 0, 0), (-1, 0), (-1, 1)], # z
    [( 0,-1), ( 0, 0), ( 0, 1), ( 1, 1)], # L
    [( 0,-1), ( 0, 0), ( 0, 1), (-1, 1)], # inverse L
    [( 0,-1), (-1, 0), ( 0, 0), ( 1, 0)] # T
]

def main():
    app = QApplication(sys.argv)
    game = Game((WIDTH, HEIGHT), INTERVAL, STEP_TIME, BLOCKS, TICK_INCREASE)

    mainWin = QWidget()
    mainLayout = QHBoxLayout(mainWin)

    gameFrame = QFrame(mainWin)
    gameLayout = QVBoxLayout(gameFrame)
    gameFrame.setFrameStyle(QFrame.Raised | QFrame.StyledPanel)
    gameView = GameView(game, gameFrame)
    gameLayout.addWidget(gameView)
    mainLayout.addWidget(gameFrame)

    # yay... refactor me when less lazy
    nextFrame = QFrame(mainWin)
    nextLayout = QVBoxLayout(nextFrame)
    nextFrame.setFrameStyle(QFrame.Raised | QFrame.StyledPanel)
    nextLabel = QLabel("<b>Next Block</b>", nextFrame)
    nextLabel.setAlignment(Qt.AlignCenter)
    nextLayout.addWidget(nextLabel)
    nextView = NextBlockView(game, nextFrame)
    nextLayout.addWidget(nextView)
    scoreLabel = QLabel("<b>Score</b>", nextFrame)
    scoreLabel.setAlignment(Qt.AlignCenter)
    nextLayout.addWidget(scoreLabel)
    scoreLabel = ScoreView(game, nextFrame)
    nextLayout.addWidget(scoreLabel)
    levelLabel = QLabel("<b>Level</b>", nextFrame)
    levelLabel.setAlignment(Qt.AlignCenter)
    nextLayout.addWidget(levelLabel)
    levelLabel = LevelView(game, nextFrame)
    nextLayout.addWidget(levelLabel)
    nextLayout.addStretch()
    mainLayout.addWidget(nextFrame)

    mainWin.setWindowTitle("Therapy :: Sirtet")
    mainWin.show()
    game.start()
    app.exec_()

if __name__ == "__main__":
    main()

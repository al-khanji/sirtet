# Copyright (C) 2008 Louai "slougi" Al-Khanji <louai.khanji@gmail.com>

# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely without any restrictions.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import resources

import game

class LevelView(QWidget):
    def __init__(self, game, *args):
        QWidget.__init__(self, *args)
        self.game = game
        self.game.registerView(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        l = QHBoxLayout()
        l.addWidget(self.label)
        self.setLayout(l)
        self.tock()

    def tock(self, forced=False):
        self.label.setText(str(self.game.level))

class ScoreView(QWidget):
    def __init__(self, game, *args):
        QWidget.__init__(self, *args)
        self.game = game
        self.game.registerView(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        l = QHBoxLayout()
        l.addWidget(self.label)
        self.setLayout(l)
        self.tock()

    def tock(self, forced=False):
        self.label.setText(self.intRender(self.game.score))

    # intRender by Joachim Viide of Clarified Networks
    def intRender(self, number):
        """
        Return an unicode string representing the given number. The
        number string is grouped into chunks of max. three characters,
        e.g.:

        >>> intRender(10000)
        u'10 000'
        """

        data = unicode(number)
        bites = list()

        while data:
            bites.append(data[-3:])
            data = data[:-3]

        return " ".join(reversed(bites))


class NextBlockView(QWidget):
    def __init__(self, game, *args):
        QWidget.__init__(self, *args)
        self.game = game
        self.game.registerView(self)
        self.brick = QPixmap(":/brick.png")
        w, h = self.brick.width(), self.brick.height()
        w, h = (w + 2) * 5, (h + 2) * 5
        self.setFixedSize(w, h)
        self.setFocusPolicy(Qt.NoFocus)

    def tock(self, forced=False):
        self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        for (x, y) in self.game.next:
            x += 2
            y += 2
            x *= self.brick.width() + 2
            y *= self.brick.height() + 2
            p.drawPixmap(x, y, self.brick)
        p.end()

class GameView(QWidget):
    def __init__(self, game, *args):
        QWidget.__init__(self, *args)
        self.game = game
        self.game.registerView(self)
        self.brick = QPixmap(":/brick.png")
        w, h = self.brick.width(), self.brick.height()
        w, h = self.game.width * (w + 2) - 2, self.game.height * (h + 2) - 2
        self.setFixedSize(w, h)
        self.setFocusPolicy(Qt.StrongFocus)

    def tock(self, forced=False):
        if forced:
            self.repaint()
        else:
            self.update()

    def paintEvent(self, event):
        p = QPainter()
        p.begin(self)
        for i, row in enumerate(self.game.rows):
            y = i * (self.brick.height() + 2)
            for j in range(self.game.width):
                if row.isMarked(j):
                    x = j * (self.brick.width() + 2)
                    p.drawPixmap(x, y, self.brick)
        for (x, y) in self.game.current:
            x += self.game.column
            y += self.game.row
            x *= self.brick.width() + 2
            y *= self.brick.height() + 2
            p.drawPixmap(x, y, self.brick)

        if self.game.isOver:
            p.setPen(QPen(Qt.white))
            p.fillRect(self.rect(), QColor(0, 0, 0, 200))
            p.drawText(self.rect(), Qt.AlignCenter,
                       self.tr("GAME OVER\nclick to play again"))
        p.end()

    def mousePressEvent(self, event):
        if self.game.isOver:
            self.game.reset()
            self.game.start()

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key_Left:
            self.game.input(game.INPUT_LEFT)
        elif k == Qt.Key_Right:
            self.game.input(game.INPUT_RIGHT)
        elif k == Qt.Key_Space:
            self.game.input(game.INPUT_DROP)
        elif k == Qt.Key_Up:
            self.game.input(game.INPUT_SPIN)
        elif k == Qt.Key_Down:
            self.game.input(game.INPUT_DOWN)

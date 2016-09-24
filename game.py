# Copyright (C) 2008 Louai "slougi" Al-Khanji <louai.khanji@gmail.com>

# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.

# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely without any restrictions.

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import random

# I would love real named enums in python....
INPUT_RIGHT, INPUT_LEFT, INPUT_DOWN, INPUT_SPIN, INPUT_DROP = range(5)

class RowException(Exception):
    pass

class Row(object):
    def __init__(self, w):
        object.__init__(self)
        self.data = set()
        self.width = w

    def mark(self, pos):
        if not pos < self.width:
            raise RowException(pos, "Trying to mark invalid position")
        self.data.add(pos)

    def isMarked(self, pos):
        return pos in self.data

    def isFull(self):
        return len(self.data) == self.width

class Game(QObject):
    def __init__(self, (w, h), interval, stepTime, blocks, tickIncrease, *args):
        QObject.__init__(self, *args)

        self.width = w
        self.height = h
        self.interval = interval
        self.stepTime = stepTime
        self.blocks = blocks
        self.tickIncrease = tickIncrease

        self.visuals = set() # registered visuals

        self.reset()

    def reset(self):
        self.time = self.stepTime # step time
        self.current = None # current block
        self.next = random.choice(self.blocks) # next block
        self.collisions = 0 # number of collisions so far
        self.ticks = 0 # number of ticks so far
        self.timerId = None # our timer id, None if not running
        self.score = 0
        self.isOver = False
        self.level = 1

        # assign blocks
        self.nextBlock()

        # first row is top, last is bottom
        # doesn't contain currently falling blocks
        self.rows = [Row(self.width) for _ in range(self.height)]
        self.updateVisuals()

    def start(self):
        self.killAndSetTimerId(self.startTimer(self.interval))

    def pause(self):
        self.killAndSetTimerId(None)

    def killAndSetTimerId(self, timerId):
        if self.timerId:
            self.killTimer(self.timerId)
        self.timerId = timerId

    def timerEvent(self, event):
        if event.timerId() == self.timerId:
            self.time -= self.interval
            if self.time <= 0:
                self.tick()
                self.time = self.stepTime
                self.updateVisuals()

    def registerView(self, v):
        self.visuals.add(v)

    def updateVisuals(self, forced=False):
        for v in self.visuals:
            v.tock(forced)

    def tick(self):
        collision = False
        self.ticks += 1
        for x, y in self.current:
            # we add 1 because we want to check the *next* row
            row = y + self.row + 1
            column = x + self.column
            if row < 0:
                continue
            if row == self.height or self.rows[row].isMarked(column):
                collision = True
                self.collisions += 1
                break

        if collision is True:
            for x, y in self.current:
                row = y + self.row
                column = x + self.column
                if row < 0:
                    self.pause()
                    self.isOver = True
                    return
                self.rows[row].mark(column)

            for row in list(self.rows):
                removed = 0
                if row.isFull():
                    self.rows.remove(row)
                    removed += 1
                for i in range(removed):
                    self.rows.insert(0, Row(self.width))
                if removed > 0:
                    self.score += ((removed * 10) ** 2) + self.collisions

            self.nextBlock()
        else:
            self.row += 1

    def nextBlock(self):
        self.current = self.next
        self.next = random.choice(self.blocks)
        self.row = -max([y for x, y in self.current]) - 1
        self.column = self.width / 2

        if self.ticks >= self.tickIncrease:
            self.ticks = 0
            self.level += 1
            self.stepTime -= self.stepTime / 10
            self.updateVisuals()

    def move(self, amount):
        self.column += amount
        for x, y in self.current:
            col = self.column + x
            row = self.row + y
            if col < 0 or col >= self.width or \
               (self.rows[row].isMarked(col) and row >= 0):
                self.column += -amount
                break

    def spin(self):
        self.current = [(-y, x) for x, y in self.current]
        for x, _ in self.current:
            col = self.column + x
            if col < 0 or col >= self.width:
                self.move(-x)

    def input(self, i):
        if self.timerId is not None:
            if i == INPUT_LEFT:
                self.move(-1)
            elif i == INPUT_RIGHT:
                self.move(1)
            elif i == INPUT_DROP:
                c = self.collisions
                while c == self.collisions:
                    self.tick()
                    self.updateVisuals(forced=True)
                self.time = self.stepTime
            elif i == INPUT_SPIN:
                self.spin()
            elif i == INPUT_DOWN:
                self.tick()
                self.time = self.stepTime
            self.updateVisuals()

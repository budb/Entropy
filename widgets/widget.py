from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QPoint, Qt
from PyQt5 import QtGui, QtCore
from urllib import request

import pyowm, logging, threading, urllib, pytz

class Widget(QWidget):
    global oldEvent

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

    def configure(self):
        # position
        if 'position' in self.args:
            if self.args['position'] == 'center':
                desktopRect = QApplication.desktop().availableGeometry(self)
                self.parentWidget().move((desktopRect.width() * 0.5) - (self.width() * 0.25),
                                         (desktopRect.height() * 0.5) - (self.height() * 0.25))
            elif (self.args['position'][0] >= 0) & (self.args['position'][1] >= 0):
                self.parentWidget().move(self.args['position'][0], self.args['position'][1])

    def mousePressEvent(self, event):
        super(Widget, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.oldEvent = QPoint(event.globalPos())

    def mouseMoveEvent(self, event):
        super(Widget, self).mouseMoveEvent(event)
        newEvent = QPoint(event.globalPos())
        delta = (newEvent - self.oldEvent)
        new_Pos = (self.parentWidget().pos() + delta)
        self.parentWidget().move(new_Pos)
        self.oldEvent = QPoint(event.globalPos())

    def mouseReleaseEvent(self, event):
        super(Widget, self).mouseReleaseEvent(event)
        self.leftClick = False
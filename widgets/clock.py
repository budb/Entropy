from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtCore import QPoint
import time, logging

class DigClock(QLCDNumber):
    global oldEvent

    def __init__(self, parent=None):
        super(DigClock, self).__init__(parent)

        localtime = time.strftime("%H:%M")
        self.display(localtime)
        logging.info('Time ' + localtime)
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #transparency
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        super(DigClock, self).mousePressEvent(event)
        logging.info('mousePress')
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.oldEvent=QPoint(event.globalPos())

    def mouseMoveEvent(self, event):
        newEvent = QPoint(event.globalPos())
        delta = (newEvent-self.oldEvent)
        new_Pos= (self.parentWidget().pos() + delta)

        self.parentWidget().move(new_Pos)
        self.oldEvent = QPoint(event.globalPos())

    def mouseReleaseEvent(self, event):
        super(DigClock, self).mouseReleaseEvent(event)
        logging.info('mouseRelease')
        self.leftClick = False





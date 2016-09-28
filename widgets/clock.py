from PyQt5 import QtCore
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QLCDNumber
from PyQt5.QtCore import QPoint
import time, logging, threading

class DigClock(QLCDNumber):
    global oldEvent
    global args

    def updateTime(self):
        localtime = time.strftime("%H:%M")
        self.display(localtime)

        #Calling update does not delete old active segments
        #calling parent widget to avoid graphic errors
        if self.parentWidget() is not None:
            self.parentWidget().hide()
            self.parentWidget().show()

        t = threading.Timer(5, self.updateTime)
        t.daemon = True
        t.start()


    def __init__(self, args):
        super(DigClock, self).__init__()
        self.args=args

        t=threading.Timer(0.5, self.updateTime)
        t.daemon = True
        t.start()

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #CONFIGURATION ON INITIALIZATION
        #transparency
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if 'transparency' in self.args:
            if args['transparency'] == 'True':
                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


    def configure(self):
        # position
        if 'position' in self.args:
            if self.args['position'] == 'center':
                desktopRect = QApplication.desktop().availableGeometry(self)
                self.parentWidget().move((desktopRect.width()*0.5) - (self.width() * 0.25), (desktopRect.height()*0.5) - (self.height() * 0.25))
            elif (self.args['position'][0] >= 0) & (self.args['position'][1] >= 0):
                self.parentWidget().move(self.args['position'][0], self.args['position'][1])

    def mousePressEvent(self, event):
        super(DigClock, self).mousePressEvent(event)
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
        self.leftClick = False





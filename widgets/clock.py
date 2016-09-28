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

        t = threading.Timer(5.0, self.updateTime)
        t.daemon = True
        t.start()


    def __init__(self, args):
        super(DigClock, self).__init__()
        self.args=args

        threading.Timer(1, self.updateTime()).start()
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #CONFIGURATION ON INITIALIZATION
        #transparency
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if args['transparency'] == 'True':
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)


    def configure(self):
        # position
        if 'position' in self.args:
            desktopRect = QApplication.desktop().availableGeometry(self)
            center = desktopRect.center();
            self.parentWidget().move((desktopRect.width()*0.5) - (self.width() * 0.25), (desktopRect.height()*0.5) - (self.height() * 0.25))
            #self.parentWidget().move(center.x()-(self.width()*0.4), center.y()-(self.height()*0.4))


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





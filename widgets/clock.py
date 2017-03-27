import threading
import time
import widgets.widget

from PyQt5 import QtCore
from PyQt5.Qt import QApplication, QStackedLayout
from PyQt5.QtWidgets import QLCDNumber


class DigClock(widgets.widget.Widget):
    global args
    global mainW

    def updateTime(self):
        localtime = time.strftime("%H:%M")
        self.mainW.display(localtime)

        self.update()

        t = threading.Timer(5, self.updateTime)
        t.daemon = True
        t.start()


    def __init__(self, args):
        super(DigClock, self).__init__()
        self.args=args

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #CONFIGURATION ON INITIALIZATION
        #background
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #main widget
        self.mainW= QLCDNumber()

        #main layout
        mainL = QStackedLayout()
        mainL.addWidget(self.mainW)
        self.setLayout(mainL)

        t = threading.Timer(0.5, self.updateTime)
        t.daemon = True
        t.start()

        bg = ""
        mc = ""
        if 'background' in self.args:
            if args['background'] == 'transparent':
                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            if self.args['background'][0] == '#':
                bg = "background-color:" + self.args['background'] + ";"

        if 'color' in self.args:
            mc = "color: " + self.args['color'] + ";"

        self.setStyleSheet("QWidget"
                        "{"+
                        bg +
                        mc +
                        "}")

    def configure(self):
        # position
        if 'position' in self.args:
            if self.args['position'] == 'center':
                desktopRect = QApplication.desktop().availableGeometry(self)
                self.parentWidget().move((desktopRect.width()*0.5) - (self.width() * 0.25), (desktopRect.height()*0.5) - (self.height() * 0.25))
            elif (self.args['position'][0] >= 0) & (self.args['position'][1] >= 0):
                self.parentWidget().move(self.args['position'][0], self.args['position'][1])






from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.Qt import QApplication
from PyQt5.QtCore import QPoint, Qt
from PyQt5 import QtGui, QtCore
from urllib import request

import pyowm, logging, threading, urllib, pytz

class Sign(QWidget):
    global oldEvent
    global text
    global mode
    global args
    global mode_nr

    def updateTask(self):
        self.text.setText("Test")
        # Update each 10 min
        t = threading.Timer(600, self.updateTask)
        t.daemon = True
        t.start()

    def __init__(self, w_args, parent=None):
        super(Sign, self).__init__(parent)
        self.args = w_args
        self.mode_nr = 0
        self.text = QLabel(self.args['text'][self.mode_nr])
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setWordWrap(True);
        self.mode = QPushButton("Mode")
        self.mode.clicked.connect(self.changeMode)

        #Set button size
        button_text_size = ''
        if 'button_size' in self.args:
            button_text_size = "font-size:"+w_args['button_size']+";"
            print(button_text_size)

        self.mode.setStyleSheet(
            "QWidget.QPushButton "
            "{ background-color: rgba(0, 0, 0, 20%); "
            +button_text_size+
            "border:1px solid rgb(100, 100, 100); }"

            "QWidget.QPushButton:pressed "
            "{ background-color: rgba(0, 0, 0, 50%); "
            "border:1px solid rgb(205, 205, 205); }"
        )

        # Add
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.text)
        mainLayout.addWidget(self.mode)

        mainW = QWidget()
        mainW.setLayout(mainLayout)
        mainL = QHBoxLayout()
        mainL.setContentsMargins(0, 0, 0, 0)
        mainL.addWidget(mainW)

        self.setLayout(mainL)

        mainW.setObjectName("Container")

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        # background
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        bg = ""
        if 'background' in self.args:
            if w_args['background'] == 'transparent':
                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            if w_args['background'][0] == '#':
                bg = "background-color:" + self.args['background'] + ";"
                pass

        mainW.setStyleSheet("QWidget#Container"
                            "{border-style: outset;" +
                            bg +
                            "border-width: 1px;"
                            "border-color: rgb(60, 60, 60);"
                            "}")
        # text color
        ct = ''
        if 'color' in self.args:
            ct = "color: " + w_args['color'] + ";"
        # text-size
        ts = ''
        if 'font_size' in self.args:
            ts = "font-size: " + w_args['font_size'] + ";"
        self.setStyleSheet(ct + ts)

    def changeMode(self):
        self.text.setText(self.args['text'][self.mode_nr])
        self.mode_nr += 1
        if self.mode_nr >= len(self.args['text']):
            self.mode_nr = 0

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
        super(Sign, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.oldEvent = QPoint(event.globalPos())

    def mouseMoveEvent(self, event):
        super(Sign, self).mouseMoveEvent(event)
        newEvent = QPoint(event.globalPos())
        delta = (newEvent - self.oldEvent)
        new_Pos = (self.parentWidget().pos() + delta)
        self.parentWidget().move(new_Pos)
        self.oldEvent = QPoint(event.globalPos())

    def mouseReleaseEvent(self, event):
        super(Sign, self).mouseReleaseEvent(event)
        self.leftClick = False
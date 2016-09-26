from PyQt5.QtWidgets import QWidget, QLCDNumber, QLabel
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5 import QtGui, QtCore

import pyowm, yaml, logging


class Weather(QLabel):

    def __init__(self, parent=None):
        super(Weather, self).__init__(parent)

        with open("config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile)

        owm = pyowm.OWM(cfg['weather']['api_key'])
        observation = owm.weather_at_id(2911298)
        self.setText("Test")
        w = observation.get_weather()
        self.setText("Weather: " + w.get_detailed_status())
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color:transparent;")

    def mousePressEvent(self, event):
        super(Weather, self).mousePressEvent(event)
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
        super(Weather, self).mouseReleaseEvent(event)
        logging.info('mouseRelease')
        self.leftClick = False



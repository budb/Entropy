from PyQt5.QtWidgets import QWidget, QLCDNumber, QLabel
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5 import QtGui, QtCore

import pyowm, yaml, logging, _thread


class Weather(QLabel):

    def updateWeatherTask(self, api_key, place_id):
        owm = pyowm.OWM(api_key)
        observation = owm.weather_at_id(place_id)
        logging.info('updateWeatherTask ' + str(observation))
        w = observation.get_weather()
        self.setText("Weather: " + w.get_detailed_status())

    def __init__(self, args, parent=None):
        super(Weather, self).__init__(parent)

        self.setText("Updating...")
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #Start weatherupdatetask as thread
        _thread.start_new_thread(self.updateWeatherTask, (str(args['api_key']), args['place_id']))

        #transparency
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if args['transparency'] == 'True':
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def configure(self):
        # position
        print(str(self.parentWidget()))


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



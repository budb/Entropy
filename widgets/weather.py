from PyQt5.QtWidgets import QWidget, QLCDNumber, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5 import QtGui, QtCore
from urllib import request

import pyowm, yaml, logging, threading, urllib


class Weather(QWidget):

    global oldEvent
    global status
    global temperature
    global recept_time
    global weather_icon


    def updateWeatherTask(self, api_key, place_id):
        owm = pyowm.OWM(api_key)
        observation = owm.weather_at_id(place_id)
        logging.info('updateWeatherTask ' + str(observation))
        w = observation.get_weather()

        self.status.setText(w.get_detailed_status())

        temp = w.get_temperature(unit='celsius')
        self.temperature.setText("max "+ str(temp['temp_max']) + " curr. " + str(temp['temp']) + " min " + str(temp['temp_min']))

        self.recept_time.setText(observation.get_reception_time(timeformat='iso'))

        url = 'http://openweathermap.org/img/w/'+w.get_weather_icon_name()+'.png'
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather_icon.setPixmap(pixmap)

        #Update each hour
        t = threading.Timer(3600, self.updateWeatherTask, (api_key, place_id))
        t.daemon = True
        t.start()


    def __init__(self, args, parent=None):
        super(Weather, self).__init__(parent)

        #Initialize
        title = QLabel("Weather")
        self.status = QLabel("Updating")
        self.temperature = QLabel("....")
        self.recept_time = QLabel("....")

        url = 'http://openweathermap.org/img/w/01d.png'
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather_icon = QLabel()
        self.weather_icon.setPixmap(pixmap)


        #Add
        vLayout = QVBoxLayout()
        vLayout.addWidget(title)
        vLayout.addWidget(self.status)
        vLayout.addWidget(self.temperature)
        vLayout.addWidget(self.recept_time)
        vLayout.addWidget(self.weather_icon)
        self.setLayout(vLayout)

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #Start weatherupdatetask as thread
        t = threading.Timer(1.0, self.updateWeatherTask, (str(args['api_key']),args['place_id']))
        t.daemon = True
        t.start()


        #transparency
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        if args['transparency'] == 'True':
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def configure(self):
        #self.setStyleSheet("background-color:transparent;")
        #self.parentWidget().setStyleSheet("background-color:transparent; "
        #"border:1px solid rgb(100, 100, 100); ")
        pass

    def mousePressEvent(self, event):
        super(Weather, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.oldEvent=QPoint(event.globalPos())


    def mouseMoveEvent(self, event):
        newEvent = QPoint(event.globalPos())
        if self.oldEvent is not None:
            delta = (newEvent-self.oldEvent)
            new_Pos= (self.parentWidget().pos() + delta)
            self.parentWidget().move(new_Pos)
            self.oldEvent = QPoint(event.globalPos())
        else:
            self.oldEvent = QPoint(event.globalPos())

    def mouseReleaseEvent(self, event):
        super(Weather, self).mouseReleaseEvent(event)
        self.leftClick = False






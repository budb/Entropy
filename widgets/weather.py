from PyQt5.QtWidgets import QWidget, QLCDNumber, QPushButton, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtGui import QPalette
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5 import QtGui, QtCore
from urllib import request

import pyowm, yaml, logging, threading, urllib


class Weather(QWidget):

    global oldEvent
    global status
    global status_text
    global temperature
    global recept_time
    global weather_icon


    def updateWeatherTask(self, api_key, place_id):
        owm = pyowm.OWM(api_key)
        observation = owm.weather_at_id(place_id)
        logging.info('updateWeatherTask ' + str(observation))
        w = observation.get_weather()

        self.status_text.setText(w.get_detailed_status())

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

        self.status_text = QLabel("Updating")
        self.temperature = QLabel("....")
        self.recept_time = QLabel("....")

        url = 'http://openweathermap.org/img/w/01d.png'
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather_icon = QLabel()
        self.weather_icon.setPixmap(pixmap)

        self.status = QWidget()
        stat_layout = QHBoxLayout()
        stat_layout.addWidget(self.status_text)
        stat_layout.addWidget(self.weather_icon)
        stat_layout.setContentsMargins(0, 0, 0, 0)
        self.status.setLayout(stat_layout)

        #
        # Add
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.status)
        mainLayout.addWidget(self.temperature)
        mainLayout.addWidget(self.recept_time)

        mainW = QWidget()
        mainW.setLayout(mainLayout)
        mainL = QHBoxLayout()
        mainL.setContentsMargins(0,0,0,0)
        mainL.addWidget(mainW)

        self.setLayout(mainL)

        mainW.setObjectName("Container")
        mainW.setStyleSheet("QWidget#Container"
                   "{border-style: outset;"
                    "border-width: 1px;"
                    "border-color: rgb(60, 60, 60);"
                    "}")

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
        pass

    def mousePressEvent(self, event):
        super(Weather, self).mousePressEvent(event)
        print("Press")
        if event.button() == QtCore.Qt.LeftButton:
            self.leftClick = True
            self.oldEvent=QPoint(event.globalPos())


    def mouseMoveEvent(self, event):
        super(Weather, self).mouseMoveEvent(event)
        newEvent = QPoint(event.globalPos())
        delta = (newEvent - self.oldEvent)
        new_Pos = (self.parentWidget().pos() + delta)
        self.parentWidget().move(new_Pos)
        self.oldEvent = QPoint(event.globalPos())

    def mouseReleaseEvent(self, event):
        super(Weather, self).mouseReleaseEvent(event)
        self.leftClick = False

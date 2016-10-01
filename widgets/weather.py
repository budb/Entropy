from PyQt5.QtWidgets import QWidget, QLCDNumber, QPushButton, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5 import QtGui, QtCore
from urllib import request

import pyowm, logging, threading, urllib, datetime, pytz, widgets.widget


class Weather(widgets.widget.Widget):

    global oldEvent
    global status
    global status_text
    global temperature
    global recept_time
    global weather_icon
    global args

    def updateWeatherTask(self):
        api_key = str(self.args['api_key'])
        place_id = self.args['place_id']

        owm = pyowm.OWM(api_key)
        observation = owm.weather_at_id(place_id)
        logging.info('updateWeatherTask ' + str(observation))
        w = observation.get_weather()

        self.status_text.setText(w.get_detailed_status())

        temp = w.get_temperature(unit='celsius')
        self.temperature.setText("max "+ str(temp['temp_max']) + " curr. " + str(temp['temp']) + " min " + str(temp['temp_min']))

        #Handle time conversion
        dtime_utc = (observation.get_reception_time(timeformat='date')).replace(tzinfo=pytz.timezone('UTC'))
        dtime_local = dtime_utc.astimezone(pytz.timezone('Europe/Berlin'))
        self.recept_time.setText(dtime_local.strftime("%Y-%m-%d %H:%M:%S %Z%z"))

        #Get weather icon
        url = 'http://openweathermap.org/img/w/'+w.get_weather_icon_name()+'.png'
        data = urllib.request.urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.weather_icon.setPixmap(pixmap)

        #Update each 10 min
        t = threading.Timer(600, self.updateWeatherTask)
        t.daemon = True
        t.start()
        return 1

    def __init__(self, w_args, parent=None):
        super(Weather, self).__init__(parent)
        self.args = w_args

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


        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

        #Start weatherupdatetask as thread
        t = threading.Timer(1.0, self.updateWeatherTask)
        t.daemon = True
        t.start()

        #background
        self.setAutoFillBackground(True)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        bg = ""
        if 'background' in self.args:
            if w_args['background'] == 'transparent':
                self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            if w_args['background'][0] == '#':
                bg = "background-color:"+self.args['background']+";"
                pass

        mainW.setStyleSheet("QWidget#Container"
                            "{border-style: outset;" +
                            bg +
                            "border-width: 1px;"
                            "border-color: rgb(60, 60, 60);"
                            "}")

        #text color
        ct = ''
        if 'color' in self.args:
            ct = "color: " + w_args['color'] + ";"

        #text-size
        ts = ''
        if 'font_size' in self.args:
            ts = "font-size: " + w_args['font_size'] + ";"

        self.setStyleSheet(ct+ts)



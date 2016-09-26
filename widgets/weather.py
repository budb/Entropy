from PyQt5.QtWidgets import QWidget, QLCDNumber, QLabel
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtCore
import time, logging, pyowm
import yaml

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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color:transparent;")


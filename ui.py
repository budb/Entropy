import logging, yaml, importlib

from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QPoint


class FloatArea(QMdiArea):

    global label
    _modules = []
    _widgets = []
    global cfg

    def __init__(self, parent=None):
        super(FloatArea, self).__init__(parent)
        self.maximumSize()

        label = QLabel("")
        label.setStyleSheet("QLabel"
                         "{ border-image: url(./wallpaper.jpg); "
                         "border:1px solid rgb(255, 170, 255); }")

        self._blub = self.addSubWindow(label, Qt.FramelessWindowHint| Qt.WindowDoesNotAcceptFocus)
        self._blub.setFocusPolicy(Qt.NoFocus)

        self.initWidgets()


    def resizeEvent(self, QResizeEvent):
        logging.info('Area.resizeEvent central widget size w ' + str(self.width()) + " h " + str(self.width()))
        self._blub.resize(self.width(),self.height())

    def importWidget(self, index, key):
        logging.info(key)
        logging.info(index)
        logging.info(self.cfg['widgets'][key])

        #Import modules
        self._modules.append(importlib.import_module('widgets.'+key))
        logging.info("module " + str(self._modules[index]))

        #Create and store instance
        self._widgets.append(getattr(self._modules[index], self.cfg['widgets'][key])())

        #Add widget to main window
        logging.info("widgets " + str(self._widgets[index]))
        _subwindow = self.addSubWindow(self._widgets[index])
        _subwindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        pass

    def initWidgets(self):

        with open("config.yml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)

        for index, key in enumerate(self.cfg['widgets']):
            self.importWidget(index, key)




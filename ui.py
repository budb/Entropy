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
        with open("config.yml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)

        self.maximumSize()
        self.setupBackground()
        self.initWidgets()

    def setupBackground(self):
        label = QLabel("")
        if 'background' in self.cfg['general']:
            if self.cfg['general']['background'][0] == '#':
                label.setStyleSheet("QLabel"
                                    "{ background-color: " +
                                    self.cfg['general']['background'] + "; "
                                    "border:1px solid rgb(0,0,0); }")
            else:
                print(self.cfg['general']['background'][0])
                label.setStyleSheet("QLabel"
                                    "{ border-image: url("+
                                    self.cfg['general']['background']+"); "
                                    "border:1px solid rgb(0,0,0); }")

        self._blub = self.addSubWindow(label, Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus)
        self._blub.setFocusPolicy(Qt.NoFocus)

    def resizeEvent(self, QResizeEvent):
        logging.info('Area.resizeEvent central widget size w ' + str(self.width()) + " h " + str(self.width()))
        self._blub.resize(self.width(),self.height())

    def importWidget(self, index, key):
        logging.info(self.cfg['widgets'][key]['class'])

        #Import modules
        self._modules.append(importlib.import_module('widgets.'+key))
        logging.info("module " + str(self._modules[index]))

        #Create and store instance
        self._widgets.append(getattr(self._modules[index], self.cfg['widgets'][key]['class'])(self.cfg['widgets'][key]))

        #Add widget to main window
        logging.info("widgets " + str(self._widgets[index]))
        _subwindow = self.addSubWindow(self._widgets[index])

        #Set subwindow containing widget transparent
        _subwindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        _subwindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._widgets[index].configure()


    def initWidgets(self):
        for index, key in enumerate(self.cfg['widgets']):
            logging.info("index " + str(index) + ' key ' + key)
            self.importWidget(index, key)




#!/usr/bin/env python3
import sys, logging, ui, yaml

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication

class Entropy(QMainWindow):
    """
    Base class

    Initializes the main window. Program logic is handled in the ui class.
    """
    global cfg

    def __init__(self):
        super().__init__()
        with open("config.yml", 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)
        self.initUI()

    def initUI(self):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info('Entropy.InitUI')

        self.setWindowTitle('ENTROPY')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.resize(self.maximumHeight(), self.maximumWidth())

        if 'frameless' in self.cfg['general']:
            if self.cfg['general']['frameless'] == 'True':
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        _mdi = ui.FloatArea(self)
        self.setCentralWidget(_mdi)


    def resizeEvent(self, QResizeEvent):
        logging.info('Entropy.resizeEvent central widget size w ' + str(self.centralWidget().width()) + " h " + str(self.centralWidget().height()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Entropy()
    ex.show()
    sys.exit(app.exec_())




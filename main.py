#!/usr/bin/env python3
import logging
import sys
from base64 import _85encode

import ui
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPalette, QBrush
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QLineEdit, \
    QPushButton, QMessageBox, QMainWindow, QApplication, QSizePolicy

class Entropy(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info('Entropy.InitUI')

        self.setWindowTitle('ENTROPY')
        self.resize(self.maximumHeight(), self.maximumWidth())

        logging.info('Entropy.InitUI self max w ' + str(self.maximumHeight()) + " max h " + str(self.maximumWidth()))

        _mdi = ui.FloatArea(self)
        self.setCentralWidget(_mdi)

        logging.info('Entropy.InitUI central widget size w ' + str(self.centralWidget().width()) + " h " + str(self.centralWidget().height()))

        button_settings = QPushButton("settings")
        button_settings.setStyleSheet(
            "QWidget.QPushButton "
            "{ background-color: rgba(0, 0, 0, 20%); "
            "border:1px solid rgb(100, 100, 100); }"

            "QWidget.QPushButton:pressed "
            "{ background-color: rgba(0, 0, 0, 50%); "
            "border:1px solid rgb(205, 205, 205); }"
        )
        button_settings.clicked.connect(self.openSettings)
        self.statusBar().addWidget(button_settings)


    def resizeEvent(self, QResizeEvent):
        logging.info('Entropy.resizeEvent central widget size w ' + str(self.centralWidget().width()) + " h " + str(self.centralWidget().height()))

    def openSettings(self):
        logging.info("Entropy.openSettings ")
        settings = QMessageBox()
        settings.setText("setup")
        settings.setInformativeText("settings will go here")
        settings.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Entropy()
    ex.show()
    sys.exit(app.exec_())




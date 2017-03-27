import random
import threading

import yaml

import widgets.widget

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout

quotes_list = []
fakeAuthorList = []

class Quotes(widgets.widget.Widget):
    global quote
    global author
    global args

    global data

    def updateQuoteTask(self):
        choice=random.randint(0, len(quotes_list))
        self.quote.setText(quotes_list[choice][1])
        # real or fake mode
        if self.realAuthors == 'True':
            self.author.setText(quotes_list[choice][0])
        else:
            self.author.setText(fakeAuthorList[random.randint(0, len(quotes_list))])

        #Update each 12 h
        t = threading.Timer(43200, self.updateQuoteTask)
        t.daemon = True
        t.start()
        return 1

    def __init__(self, w_args, parent=None):
        super(Quotes, self).__init__(parent)
        self.args = w_args

        with open("static.yml", 'r') as ymlfile:
            self.data = yaml.load(ymlfile)

        # Load quotes and authors
        for key in self.data['quotes']['list']:
            #print(key, self.data['quotes']['list'][key])
            quotes_list.append([key, self.data['quotes']['list'][key]])

        for key in self.data['quotes']['fake_authors']:
            #print(key, self.data['quotes']['list'][key])
            fakeAuthorList.append(key)


        self.quote = QLabel("Updating")
        self.author = QLabel("....")

        self.author.setAlignment(QtCore.Qt.AlignBottom)
        self.quote.setWordWrap(True)   
        self.quote.setAlignment(QtCore.Qt.AlignTop)


        # Add widgets to layout
        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(0)
        mainLayout.addWidget(self.quote)
        mainLayout.addWidget(self.author) 

        mainW = QWidget()
        mainW.setLayout(mainLayout)

        mainL = QHBoxLayout()
        mainL.setContentsMargins(0,0,0,0)
        mainL.addWidget(mainW)

        self.setLayout(mainL)

        mainW.setObjectName("Container")

        # Fake or normal mode 
        if 'mode' in self.args:
            self.realAuthors=w_args['mode']

        #Start updatetask as thread
        t = threading.Timer(1.0, self.updateQuoteTask)
        t.daemon = True
        t.start()

        self.setMinimumHeight(200)
        self.setMinimumWidth(400)

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



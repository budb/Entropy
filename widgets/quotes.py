from PyQt5.QtWidgets import QWidget, QLCDNumber, QPushButton, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5 import QtGui, QtCore
from urllib import request

import pyowm, logging, threading, urllib, datetime, pytz, widgets.widget, random

class Quotes(widgets.widget.Widget):
    global quote
    global author
    global args
    global quoteList
    global realAuthors

    def updateQuoteTask(self):
        choice=random.randint(0, len(self.quoteList))
        self.quote.setText(self.quoteList[choice])
        # real or fake mode
        if self.realAuthors == 'True':
            self.author.setText(self.authorList[choice])
        else:
            self.author.setText(self.fakeAuthorList[random.randint(0, len(self.quoteList))])

        #Update each 12 h
        t = threading.Timer(43200, self.updateQuoteTask)
        t.daemon = True
        t.start()
        return 1

    def __init__(self, w_args, parent=None):
        super(Quotes, self).__init__(parent)
        self.args = w_args
        self.quoteList=["Genie ist Fleiß", 
                        "Wir können den Wind nicht ändern, aber die Segel anders setzen.",
                        "Jeder, der sich die Fähigkeit erhält, Schönes zu erkennen, wird nie alt werden.",
                        "Der erste Schritt zur Philosophie ist der Unglaube.",
                        "Zwei Wahrheiten können einander nie widersprechen.",
                        "Der größte Lump im ganzen Land, das ist und bleibt der Denunziant."
                        "Der Worte sind genug gewechselt, Laßt mich auch endlich Taten sehn!",
                        "Die Botschaft hör´ ich wohl, allein mir fehlt der Glaube",
                        "Man muß die Dinge so einfach wie möglich machen. Aber nicht einfacher."
                        "Jedes Volk hat die Regierung, die es verdient."    #10       
                        "Man erkennt den Charakter eines Menschen an den Späßen, über die er lacht.",
                        "Eine falsche Ansicht zu widerrufen erfordert mehr Charakter, als sie zu verteidigen.",    
                        "Der Mensch ist zur Freiheit verurteilt.",
                        "Clothes make the man. Naked people have little or no influence on society.",
                        "Shortcuts make long delays",
                        "Impossible is a word that humans use far too often.",     
                        ]

        self.authorList=["Johann Wolfgang von Goethe", 
                        "Aristoteles",
                        "Franz Kafka",
                        "Denis Diderot",
                        "Galileo Galilei",
                        "August Heinrich Hoffmann von Fallersleben",
                        "Johann Wolfgang von Goethe",
                        "Faust - Johann Wolfgang von Goethe",
                        "Albert Einstein",
                        "Joseph Marie de Maistre",                          #10
                        "Alfred Biolek",
                        "Arthur Schopenhauer",
                        "J.P. Sartre",
                        "Mark Twain",
                        "J.R.R. Tolkien",
                        "Seven of Nine",
                        ]

        self.fakeAuthorList=["Lukas Podolski", 
                        "Scooter",
                        "Dieter Bohlen",
                        "Heidi Klum",
                        "Thomas Gottschalk",
                        "Deichkind",
                        "Sheldon Cooper",
                        "Batman",
                        "Paul Jahnke",
                        "Tony Stark",                          #10
                        "Olivia Jones",
                        "Christiano Ronaldo",
                        "Gina Lisa",
                        "Pietro Lombardi",
                        "Micaela Schäfer",
                        ]

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



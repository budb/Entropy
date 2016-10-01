import socket, logging
from PyQt5.QtWidgets import QWidget

class Network(QWidget):

    def __init__(self, args):
        super(Network, self).__init__()
        logging.info("open network")

    def neighbors(self):
        logging.info("search neighbors")
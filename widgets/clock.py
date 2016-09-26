from PyQt5.QtWidgets import QLCDNumber
import time, logging

class DigClock(QLCDNumber):

    def __init__(self, parent=None):
        super(DigClock, self).__init__(parent)

        localtime = time.strftime("%H:%M")
        self.display(localtime)
        logging.info('Time ' + localtime)
        self.setMinimumHeight(200)
        self.setMinimumWidth(400)


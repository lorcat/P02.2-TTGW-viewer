__author__ = 'Konstantin Glazyrin'

from time import sleep

from app.common.features import Tester
from PyQt4 import QtCore, QtGui

class MMEvent(QtCore.QObject, Tester):
    sign_wdgts = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        Tester.__init__(self)
        QtCore.QObject.__init__(self, parent=parent)

    def report(self, func):
        """
        Creates a signal and fires the submitted function, after that the function is disconnected
        :param func:
        :return:
        """
        self.debug("Reports an event and starts a function to be fired")
        sign = QtCore.pyqtSignal(object)
        sign.connect(func)
        sign.emit()

        sleep(0.2)
        sign.disconnect(func)

MMEVENT = None

def get_mm():
    global MMEVENT
    if MMEVENT is None:
        MMEVENT = MMEvent()
    return MMEVENT

get_mm()
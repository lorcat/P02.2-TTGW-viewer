__author__ = 'glazyrin'

from PyQt4 import QtGui, QtCore

from app.config.keys import *
from app.config import configuration as config
from app.common import Tester

TEMPLATE = "Loading: {}"

class SplashWindow(QtGui.QSplashScreen, Tester):
    # signal for loading finalization
    signfinished = QtCore.pyqtSignal()

    def __init__(self):
        Tester.__init__(self)

        self.debug("Initialization")

        # pixmap for the splash screen
        fi = self._prepareImagePath()
        pixmap = QtGui.QPixmap(fi.absoluteFilePath())

        QtGui.QSplashScreen.__init__(self, pixmap=pixmap)

        self._proc = QtGui.QProgressBar()
        self._proc.setRange(0, 100)
        self._proc.setTextVisible(True)
        self._proc.setAlignment(QtCore.Qt.AlignHCenter)

        self._label = QtGui.QLabel("")

        layout = QtGui.QGridLayout(self)

        layout.addWidget(self._label, 1, 0)
        layout.addWidget(self._proc, 2, 0, 1, 2)
        layout.setVerticalSpacing(10)
        layout.setHorizontalSpacing(10)
        layout.setRowStretch(0, 50)
        layout.setColumnStretch(0, 50)
        layout.setAlignment(QtCore.Qt.AlignHCenter)

        self._step = 0

        self.show()


    @QtCore.pyqtSlot(str, int, int)
    def setProgress(self, name, value, max):
        """
        Updates progress on motor initialization
        :param name: str('Name of Motor')
        :param value: int('motor index')
        :param max: int('maximum number of motors')
        :return:
        """
        self.debug("Setting progress ({}, {}, {})".format(name, value, max))

        # change on message change
        if value <= max:
            temp = int(float(value)/float(max)*100)
            self._proc.setValue(temp)
            self._label.setText(TEMPLATE.format(name))

        # stop on maximum value
        if value == max:
            self.finish(self)
            self.signfinished.emit()
            self.hide()
            return

        self.raise_()
        self.repaint()

    def registerFinished(self, func):
        """
        Connects external function to the internal event fired at the end of operation
        :param func: function to process
        :return:
        """
        self.debug("Registering finish event")
        self.signfinished.connect(func)

    def _prepareImagePath(self):
        """
        Prepares an image path based on path
        :param path: str() - path
        :return: None or QFileInfo()
        """
        path = config.RESOURCES[RESOURCE_IMAGES]

        self.debug("Preparing image path, directory ({})".format(path))

        res = None
        dir = QtCore.QDir(path)
        temp = QtCore.QFileInfo()
        temp.setFile(dir, 'splash.png')
        if temp.isFile():
            res = temp

        return res

    def timeout(self):
        """
        Repainting on a timeout - to keep the window updated
        :return:
        """
        self.repaint()
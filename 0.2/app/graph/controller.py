__author__ = 'Konstantin Glazyrin'

from copy import deepcopy
import time
import numpy as np

from app.common.qt import QtGui, QtCore
from app.common import Tester

from app.config.keys import *
from app.config import configuration as config

from scipy import ndimage

# object controlling thread for reader
class GraphController(QtCore.QObject, Tester):
    DEFAULT_PRIORITY = QtCore.QThread.InheritPriority
    DEFAULT_THREAD_TIMEOUT = 3000

    # proxy for new data signal
    sign_newdata = QtCore.pyqtSignal(object)

    # proxy for start/stop indication to the reader obj
    sign_startstop = QtCore.pyqtSignal(bool)

    # proxy for the graph updates
    sign_updategraph = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent=parent)
        Tester.__init__(self)

        # thread
        self._runner = QtCore.QThread(parent=self)

        # object to run in the thread
        self._graph = Grapher()

        # init main events
        self.__init_events()

        # init thread
        self.__init_thread()

        # self stop - indicating to the controller necessity to pass the data for processing
        self.stop = False

    def __init_events(self):
        """
        Initializes events related to the operation
        :return:
        """
        self.debug("Initializing signals")

        # thread signals
        self.connect(self._runner, QtCore.SIGNAL("started()"), self.processThreadStart)
        self.connect(self._runner, QtCore.SIGNAL("finished()"), self.processThreadFinish)

        # reader signals - new graph after processing
        self._graph.registerUpdatedGraph(self.reportUpdatedGraph)

    def __init_thread(self):
        """
        Initializes thread
        :return:
        """
        self.debug("Initializing thread")

        priority = self.DEFAULT_PRIORITY
        try:
            priority = config.PROFILES[PROFILE_PRIORITY]
        except KeyError:
            self.error("Configuration error on profile (keys: {})".format(PROFILE_PRIORITY))
            self.error("Using default priority ({})".format(priority))

        # move to the different thread
        self._runner.start(priority)

        self._graph.moveToThread(self._runner)

        # when new data is appeared - pass it to the graph object
        self.registerNewData(self._graph.run)

    def cleanup(self):
        """
        Stops thread operation, moves object to the main thread
        :return:
        """
        # stop timer
        self.stopGraph()

        # delete thread
        if self._runner.isRunning():
            self._runner.terminate()
            self._runner.wait(self.DEFAULT_THREAD_TIMEOUT)

    def processThreadStart(self):
        self.debug("Graph Thread has started")

    def processThreadFinish(self):
        self.debug("Graph Thread has finished")

    def registerNewData(self, func):
        """
        Registers function to be fired on the new data appearance - proxy
        :return:
        """
        self.debug("Registering signal with func ({})".format(func))
        self.sign_newdata.connect(func)

    def reportNewData(self, data):
        """
        Reports new data via Qt signal to the thread processing the graph
        :param data:
        :return:
        """
        if not self.stop:
            self.debug("Reporting new data (length: {}) to be processed into a graph".format(len(data)))
            self.debug("Data: {}".format(data))
            self.sign_newdata.emit(data)

    def registerStartStop(self, func):
        """
        Registers function to be fired on the new data - proxy
        :return:
        """
        self.debug("Registering start/stop signal with func ({})".format(func))
        self.sign_startstop.connect(func)

    def reportStartStop(self, value):
        """
        Reports new data via Qt signal
        :param data:
        :return:
        """
        self.debug("Reporting start/stop signal ({}) to the graph".format(str(value)))
        self.sign_startstop.emit(value)
        self.stop = value

    @QtCore.pyqtSlot()
    def startGraph(self):
        """
        Starts the timer engaging the reader
        :return:
        """
        self.info("Enabling a channel to graph processing")
        self.stop = False

        # indicate to the reader stop signal
        self._graph.setStop(False)

    @QtCore.pyqtSlot()
    def stopGraph(self):
        """
        Stops the timer engaging the reader
        :return:
        """
        self.debug("Disabling the channel to graph processing")
        self.stop = True

        # indicate to the reader stop signal
        self._graph.setStop(True)

    def registerUpdatedGraph(self, func):
        """
        Registers notification of external objects on the graph update
        :return:
        """
        self.debug("Registering a function to be notified on graph updates {}".format(func))
        self.sign_updategraph.connect(func)

    def reportUpdatedGraph(self, data):
        """
        Reports updated graph to the interested parties - proxy function
        :param data:
        :return:
        """
        self.debug("Reporting the updated graph to the interested objects")
        self.sign_updategraph.emit(data)

# object which runs the reading operation
class Grapher(QtCore.QObject, Tester):
    # mutex timeout in ms
    MUTEX_TIMEOUT = 100

    # signal emitted at the end of the read loop
    sign_updategraph = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, controller=None):
        QtCore.QObject.__init__(self, parent=parent)
        Tester.__init__(self)

        # mutex used to test the permission for the action start
        self._access_mutex = QtCore.QMutex()
        self._block = False

        # boolean flag controlling fast stop
        self._bstop = False
        self._bstarted = False

        # image to output
        self.image = QtGui.QImage()

        # controller
        self._controller = controller

    def run(self, data):
        """
        Function to be run on the new data event
        :return:
        """

        self.info("Starting grapher action")

        # try mutex lock - if not posible return
        btest = self.tryLock()

        if btest:
            self.info("Obtained lock - reading operation has started")

            # read data
            self.prep_graph(data)

            # don't forget to unlock the mutex
            self.unlock()
        else:
            self.info("Lock was not obtained - try to adjust the polling period.")
        return

    def unlock(self):
        """
        Unlocks mutex controlling reading operation
        :return:
        """
        if self._block:
            self._access_mutex.unlock()
            self._block = False

    def tryLock(self):
        """
        Trying to set a lock to start reading operation if required
        :return:
        """
        self.debug("Trying to obtain a lock on graph operation (bstop: {})".format(self.isStopped()))

        # return by controller signal
        res = False
        if self.isStopped():
            self.debug("Stopping the operation by external command")

            return res

        # return by controller attribute
        if self.test(self._controller, GraphController) and self._controller.stop:
            self.debug("Stopping the operation by controller attribute")
            return res

        if not self._block:
            res = self._access_mutex.tryLock(self.MUTEX_TIMEOUT)
            if res:
                self._block = True
        return res

    def prep_graph(self, framedata):
        """
        Reads data and returns it
        :return:
        """
        self.debug("Making adjustments with the graph ({})".format(framedata))

        # storage for data
        images = []
        w, h = 0, 0

        data = deepcopy(framedata)

        # convert images to the nice format
        for (i, el) in enumerate(data):
            if self.test(el[DATA], np.ndarray):
                self.debug("Tranforming data ({})".format(data))
                el[DATA] = np.array(el[DATA]).astype(np.float32).transpose()

                # obtaining a subset of data for view roi
                x, y, w, h = 0, 0, el[WIDTH], el[HEIGHT]
                xr, yr = 0,0
                try:
                    x,y,w,h = el[ROI_VIEW]

                    # adjust for value uncertainty
                    if x >= el[WIDTH]:
                        x = 0
                    if y >= el[HEIGHT]:
                        y = 0

                    if x+w > el[WIDTH]:
                        w = el[WIDTH]-x
                    if y+h > el[HEIGHT]:
                        h = el[HEIGHT]-y

                    xr = np.arange(w)
                    yr = np.arange(h)
                except KeyError:
                    self.error("View roi is not initialized, using the default one")

                # ROI FIT and ROI VIEW uses same subsets - same roi
                subset = el[DATA][xr[:, None]+y, yr[None,:]+x]
                el[ROI_VIEWDATA] = deepcopy(subset)
                el[ROI_FITDATA] = deepcopy(subset)

                # calculate center of mass
                com = np.array(ndimage.center_of_mass(el[ROI_FITDATA])).astype(np.int32)

                # default values + center of masses
                fwhms_x, fwhms_y = [], []
                centers = []
                coms = []

                # we perform a fit only on intensive data
                if np.max(el[ROI_FITDATA]) - np.min(el[ROI_FITDATA]) > 30:
                    xa, xi = np.max(el[ROI_FITDATA]), np.min(el[ROI_FITDATA])
                    thresh = (xa + xi) / 2
                    thresh_low = el[ROI_FITDATA] < thresh
                    thresh_high = el[ROI_FITDATA] > thresh

                    el[ROI_FITDATA][thresh_low] = 0
                    el[ROI_FITDATA][thresh_high] = 255

                    com = np.array(ndimage.center_of_mass(el[ROI_FITDATA])).round().astype(np.int32)

                    if len(com) > 0 and self.test(com[0], np.int32):
                        coms.append(com)

                    for res in coms:
                        # found maximum in a row
                        row = el[ROI_FITDATA][com[0]:][0].flatten()
                        n1, n2 = np.arange(len(el[ROI_FITDATA])), np.array(com[1])
                        col = el[ROI_FITDATA][n1[:, None], n2].flatten()

                        diff_row = np.diff(row)
                        top, bottom = np.argmax(diff_row)+1, np.argmin(diff_row)+1

                        # found a maximum in a column
                        n1, n2 = np.arange(len(el[ROI_FITDATA])), np.array(com[1])
                        col = el[ROI_FITDATA][n1[:, None], n2].flatten()
                        diff_col = np.diff(el[ROI_FITDATA][n1[:, None], n2].flatten())
                        left, right = np.argmax(diff_col)+1, np.argmin(diff_col)+1

                        # submit information on the calculations
                        fwhms_x.append(right-left)
                        fwhms_y.append(bottom-top)
                        centers.append([abs(right+left)/2, abs(bottom + top)/2])
                else:
                    self.debug("Data is not intense enough")

                el[ROI_FITCOMS] = centers
                el[ROI_FITFWHMX] = fwhms_x
                el[ROI_FITFWHMY] = fwhms_y

        self.makeinfo("Running from a thread ({}); App. thread ({})".format(self.thread(), QtGui.QApplication.instance().thread()))
        self.reportUpdatedGraph(data)

    def registerUpdatedGraph(self, func):
        """
        Register the function to be fired on new data
        :param func:
        :return:
        """
        self.debug("Registering signal with func ({})".format(func))
        self.sign_updategraph.connect(func)

    def reportUpdatedGraph(self, data):
        """
        Reports new data via Qt signal as a deepcopy
        :param data:
        :return:
        """
        self.debug("Reporting new graph data ({})".format(str(data)))
        self.makeinfo("Running from a thread ({}); App. thread ({})".format(self.thread(),
                                                                            QtGui.QApplication.instance().thread()))
        self.sign_updategraph.emit(data)

    def isStopped(self):
        """
        Returns a stop flag
        :return:
        """
        self.debug("Testing the stop signal ({})".format(self._bstop))
        return self._bstop

    def isStarted(self):
        """
        Returns a flag indicating a command start
        :return:
        """
        return self._bstarted

    @QtCore.pyqtSlot(bool)
    def setStop(self, value):
        """
        Sets the stop flag
        :param value:
        :return:
        """
        self.debug("Setting a stop signal value ({}, test {})".format(value, self.test(value, bool)))
        if self.test(value, bool):
            self._bstop = value

            if not self._bstop:
                self.setStarted(True)

    def setStarted(self, value):
        """
        Sets or resets a flag indicating initialization phase
        :param value:
        :return:
        """
        if self.test(value, bool):
            self._bstarted = value

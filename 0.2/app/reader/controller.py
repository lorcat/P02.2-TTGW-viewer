__author__ = 'Konstantin Glazyrin'

from copy import deepcopy
import time

from app.common.qt import QtGui, QtCore
from app.common import Tester

from app.config.keys import *
from app.config import configuration as config

# object controlling thread for reader
class ReaderController(QtCore.QObject, Tester):
    DEFAULT_PRIORITY = QtCore.QThread.InheritPriority
    DEFAULT_THREAD_TIMEOUT = 3000
    DEFAULT_TIMER_DELAY = 1000

    # proxy for new data signal
    sign_newdata = QtCore.pyqtSignal(object)

    # proxy for start/stop indication to the reader obj
    sign_startstop = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        QtCore.QObject.__init__(self, parent=parent)
        Tester.__init__(self)

        # thread
        self._runner = QtCore.QThread(parent=self)

        # object to run in the thread
        self._reader = Reader()

        # timer controlling the reader
        self._timer = QtCore.QTimer(parent=self)

        # init main events
        self.__init_events()

        # init thread
        self.__init_thread()

        # self stop
        self.stop = False

        # self data
        self.current_data = None

    def __init_events(self):
        """
        Initializes events related to the operation
        :return:
        """
        self.debug("Initializing signals")

        # thread signals
        self.connect(self._runner, QtCore.SIGNAL("started()"), self.processThreadStart)
        self.connect(self._runner, QtCore.SIGNAL("finished()"), self.processThreadFinish)

        # reader signals - new data loop
        self._reader.registerNewData(self.reportNewData)

        # set interval and timer type
        self._timer.setSingleShot(False)
        try:
            self._timer.setInterval(config.PROFILES[PROFILE_START][PROFILE_DELAY])
        except KeyError:
            self.error("Configuration error on profile (keys: {}|{})".format(PROFILE_START, PROFILE_DELAY))
            self.debug("Setting default value (keys: {}|{})".format(PROFILE_DELAY,self.DEFAULT_TIMER_DELAY))
            self._timer.setInterval(self.DEFAULT_TIMER_DELAY)

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

        self._reader.moveToThread(self._runner)

        # timer signal - after moving to a different thread
        self.connect(self._timer, QtCore.SIGNAL("timeout()"), self._reader.run)

    def cleanup(self):
        """
        Stops thread operation, moves object to the main thread
        :return:
        """
        # stop timer
        self.stopReader()

        # delete object
        try:
            self._reader.deleteLater()
        except RuntimeError:
            pass

        # delete thread
        if self._runner.isRunning():
            self._runner.terminate()
            self._runner.wait(self.DEFAULT_THREAD_TIMEOUT)

    def processThreadStart(self):
        self.debug("Reading Thread has started")

    def processThreadFinish(self):
        self.debug("Reading Thread has finished")

    def registerNewData(self, func):
        """
        Registers function to be fired on the new data - proxy
        :return:
        """
        self.debug("Registering signal with func ({})".format(func))
        self.sign_newdata.connect(func)

    def reportNewData(self, data):
        """
        Reports new data via Qt signal
        :param data:
        :return:
        """

        self.debug("Reporting new data ({}) by reader".format(str(data)))
        self.sign_newdata.emit(data)

        # keep a copy of data and release old one
        # temp = self.current_data
        self.current_data = deepcopy(data)
        # del temp[:]

    def repeatLastFrame(self, nick, roi):
        """
        Repeats the last data frame - inserts new frame to the queue - for roi change purposes
        :param data:
        :return:
        """
        self.debug("Updating last data frame ({}:{}:nick {})".format(self.isTimerWorking(), self.current_data, nick))

        if not self.isTimerWorking() and self.test(self.current_data):
            # update roi for the last frame
            for (i, el) in enumerate(self.current_data):
                if el[NICK] == nick:
                    temp = el[ROI_VIEW]
                    self.current_data[i][ROI_VIEW] = roi
                    del temp[:]
                    self.debug("Repeating old frame for nick ({})".format(nick))
                    self.reportNewData(self.current_data)
                    break

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
        self.debug("Reporting start/stop signal ({}) to reader".format(str(value)))
        self.sign_startstop.emit(value)

        self.stop = value

    @QtCore.pyqtSlot()
    def startReader(self):
        """
        Starts the timer engaging the reader
        :return:
        """
        self.info("Starting polling timer")
        self._timer.start()

        # indicate to the reader stop signal
        self._reader.setStop(False)

    @QtCore.pyqtSlot()
    def stopReader(self):
        """
        Stops the timer engaging the reader
        :return:
        """
        self.info("Stopping polling timer")
        self._timer.stop()

        # indicate to the reader stop signal
        self._reader.setStop(True)

    def isTimerWorking(self):
        """
        Returns if timer is working - we should get data
        :return:
        """
        return self._timer.isActive()

# object which runs the reading operation
class Reader(QtCore.QObject, Tester):
    # mutex timeout in ms
    MUTEX_TIMEOUT = 100

    # signal emitted at the end of the read loop
    sign_newread = QtCore.pyqtSignal(object)

    def __init__(self, parent=None, controller=None):
        QtCore.QObject.__init__(self, parent=parent)
        Tester.__init__(self)

        # mutex used to test the permission for the action start
        self._access_mutex = QtCore.QMutex()
        self._block = False

        # boolean flag controlling fast stop
        self._bstop = False
        self._bstarted = False

        # controller
        self._controller = controller

    def run(self):
        """
        Function to be run on the
        :return:
        """

        self.info("Starting reading action")

        # try mutex lock - if not posible return
        btest = self.tryLock()

        if btest:
            self.info("Obtained lock - reading operation has started")

            # read data
            self.read()

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
        self.debug("Trying to obtain a lock on read operation (bstop: {})".format(self.isStopped()))

        # return by controller signal
        res = False
        if self.isStopped():
            self.debug("Stopping the operation by external command")

            return res

        # return by controller attribute
        if self.test(self._controller, ReaderController) and self._controller.stop:
            self.debug("Stopping the operation by controller attribute")
            return res

        if not self._block:
            res = self._access_mutex.tryLock(self.MUTEX_TIMEOUT)
            if res:
                self._block = True
        return res

    def read(self):
        """
        Reads data and returns it
        :return:
        """
        # storage for data
        data = []

        self.makeinfo("Running from a thread ({}); App. thread ({})".format(self.thread(), QtGui.QApplication.instance().thread()))

        # get the attributes to read
        cmdloop = None

        try:
            # make a copy of a profile
            cmdloop = deepcopy(config.PROFILES[PROFILE_START][PROFILE_TANGOATTR])

            # if the start signal was obtained - initialize the device
            if self.isStarted():
                pass

        except KeyError:
            self.error("Configuration error on profile (keys: {}, {}, {})".format(PROFILE_START, PROFILE_START))
            return

        lt = time.localtime()

        # go through commands - execute one by one, save return values if needed
        for (i, el) in enumerate(cmdloop):
            self.debug("{}: {}".format(i, el))

            if self.isStopped():
                self.debug("Stopping the read operation (external signal)")
                return

            # get data nick
            nick = None
            try:
                nick = el[NICK]
            except KeyError:
                pass
            self.debug("Processing command ({} with nick {})".format(i, nick))

            # test if data requires saving
            value = None
            try:
                value = el[CMD]()
            except KeyError:
                self.error("Configuration error on command loop (keys: {})".format(CMD))

            # only valid data requires reporting - if nick is given and if the value is not None
            v, w, h = None, None, None
            if self.test(value):
                # save data
                try:
                    v, w, h = value[1], len(value[1][0]), len(value[1])
                except IndexError:
                    self.error("Strange index error on values (value indexes [1][0], [1] {})".format(value))
                    return

                roiview = [0,0,w,h]
                try:
                    roiview = el[ROI_VIEW]

                    # check that roi is within the width and height of the image
                    if roiview[2] > w:
                        roiview[2] = min(100, w)
                    if roiview[3] > h:
                        roiview[3] = min(100, h)

                    if roiview[1]+roiview[2] > w:
                        roiview[1] = w-el[ROI_VIEW][2]

                    if roiview[0]+roiview[3] > h:
                        roiview[0] = h - el[ROI_VIEW][3]

                except KeyError:
                    self.error("Configuration error on command loop (keys: {}), using default".format(ROI_VIEW))
                    pass

                penfit = [QtCore.Qt.red, 1, QtCore.Qt.SolidLine]
                try:
                    penfit = el[PENFIT]
                except KeyError:
                    self.error("Configuration error on command loop (keys: {}), using default".format(PENFIT))

                penview = [QtCore.Qt.blue, 1, QtCore.Qt.SolidLine]
                try:
                    penview = el[PENVIEW]
                except KeyError:
                    self.error("Configuration error on command loop (keys: {}), using default".format(PENVIEW))

                data.append({NICK: nick,
                             DATA: v,
                             WIDTH: w,
                             HEIGHT: h,
                             ROI_VIEW: roiview,
                             PENFIT: penfit,
                             PENVIEW: penview
                             }
                            )

                self.debug("Appending data (NICK:{})".format(nick))

        # append a date and the timestamp at the end of data accumulation
        date = "{:04}-{:02}-{:02}_{:02}:{:02}:{:02}".format(lt.tm_year, lt.tm_mon, lt.tm_mday, lt.tm_hour, lt.tm_min, lt.tm_sec)
        data.append({NICK: 'Date', DATA: date})
        data.append({NICK: TIMESTAMP, DATA: time.time()})

        # report data, clean it fast
        self.reportNewData(data)
        del data[:]

    def registerNewData(self, func):
        """
        Register the function to be fired on new data
        :param func:
        :return:
        """
        self.debug("Registering signal with func ({})".format(func))
        self.sign_newread.connect(func)

    def reportNewData(self, data):
        """
        Reports new data via Qt signal as a deepcopy
        :param data:
        :return:
        """
        self.debug("Reporting new data ({})".format(str(data)))
        temp = deepcopy(data)
        self.sign_newread.emit(temp)

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

# @TODO: report somehow the errors on unreachable devices for the person to understand
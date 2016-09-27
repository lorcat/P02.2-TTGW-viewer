__author__ = 'Konstantin Glazyrin'

from PyQt4 import QtGui, QtCore
import pickle

from app.common import *
from app.gui.gui_splash import SplashWindow
from app.gui.gui_profiledialog import ProfileDialog

from app.config.keys import *
from app.config import configuration as config

from app.reader.controller import ReaderController
from app.graph.controller import GraphController

from app.gui.main_window import MainWindow
from app.runnables import getPool

from copy import deepcopy

# main class showing the splash screen and starting main window
class Starter(QtCore.QObject, Tester):
    # delay between start of the program queue and program loading
    DELAY = 100

    # Pickle backup file template
    PROFILE_PICKLE_TEMPLATE = "{}_backup-{}.p"

    # name filters for the backup procedure
    PROFILE_PICKLE_NAME_FILTER = "{}*.p"

    # maximum number of the profiles of each kind
    PROFILES_MAX_NUMBER = 5

    def __init__(self, parent=None):
        Tester.__init__(self)
        QtCore.QObject.__init__(self, parent=parent)

        self.debug("Initializing - starting timer")
        self._timerid = self.startTimer(self.DELAY)

        # splash screen
        self._splash = None
        # main window handle
        self._mainwnd = None

        # controllers
        # reader - obtaining data
        self.ctrl_reader = None
        # writer - saving data
        self.ctrl_writer = None
        # graph controller
        self.ctrl_graph = None

        # thread pool to start one time workers
        self.thread_pool = getPool(parent=self)

    def timerEvent(self, event):
        """
        Event fired on timer - event loop engaged
        :param event:
        :return:
        """
        self.debug("Initializing - killing timer")
        self.killTimer(self._timerid)

        # selecting profile
        profile = ProfileDialog()
        res = profile.exec_()
        self.debug("Result of the profile selection ({})".format(res))
        if res == 0:
            return

        if not self.test(profile.module):
            self.exitWithError("No profile has been selected")
            return

        # populate profile information or exit
        try:
            config.PROFILES[PROFILE_START] = profile.module.START
        except AttributeError:
            msg = "The profile is malformed - no START dict()"
            QtGui.QMessageBox.critical(None, "Error", msg)
            self.exitWithError(msg)
            return

        # test profile - that necessary fields are present
        for el in [PROFILE_NAME, PROFILE_NICKNAME, PROFILE_TANGOATTR, PROFILE_DELAY, PROFILE_COLORTABLE, PROFILE_INSERTCENTER_LINES,
                   PROFILE_INSERTVIEW_LINES, PROFILE_INSERT_RECT, PROFILE_SHOW_ROIVIEW, PROFILE_CONTROLLERS]:
            try:
                v = config.PROFILES[PROFILE_START][el]
            except KeyError:
                msg = "The profile is malformed - no element ({}) is not present".format(el)
                QtGui.QMessageBox.critical(None, "Error", msg)
                self.exitWithError(msg)
                return

        # showing splash, initializing events
        self._splash = SplashWindow()
        self._splash.registerFinished(self.showMainWindow)

        # go through the initialization parts
        self.initializeApp()

    def showMainWindow(self):
        """
        Starts the main application window
        :return:
        """
        self.debug("Initializing - starting main application window")

        # create the window and register the most important events
        self._mainwnd = MainWindow(starter=self)
        self._splash.close()
        self._splash.deleteLater()

        # connect graph and the main window
        if self.test(self.ctrl_reader) and self.test(self.ctrl_graph):
            self.ctrl_graph.registerUpdatedGraph(self._mainwnd.getUpdatedGraph)

    def initializeApp(self):
        """
        Initializes controllers, main operations
        :return:
        """
        self.debug("Initializing - application (controllers, events)")

        self._splash.setProgress("restoring the profile to the latest version", 00, 100)
        self.restoreCurrentProfile()

        self._splash.setProgress("reader controller", 20, 100)
        self.ctrl_reader = ReaderController(parent=self)

        self._splash.setProgress("graph controller", 40, 100)
        self.ctrl_graph = GraphController(parent=self)

        # connect reader and writer
        if self.test(self.ctrl_reader) and self.test(self.ctrl_writer):
            self.ctrl_reader.registerNewData(self.ctrl_writer.reportNewData)

        # connect reader and graph
        if self.test(self.ctrl_reader) and self.test(self.ctrl_graph):
            self.ctrl_reader.registerNewData(self.ctrl_graph.reportNewData)

        # events
        # cleaning up upon closing the last window
        self._splash.setProgress("qt events", 90, 100)

        # cleanup procedure
        # self.connect(QtGui.QApplication.instance(), QtCore.SIGNAL("lastWindowClosed()"), self.cleanup)
        self._splash.setProgress("done", 100, 100)

    def exitWithError(self, msg):
        """
        Stops application execution and reports a message
        :param msg:
        :return:
        """
        self.debug("Exiting with an error message ({})".format(str(msg)))
        # show the error message
        self.error(msg)

        # cleanup the object
        self.cleanup()

        return

    def cleanup(self, brestart=False):
        """
        Cleans up the application
        :return:
        """
        self.debug("Exiting the application - cleaning up")

        # cleaning up the thread pool
        self.debug("Cleaning the thread pool operations")
        if self.test(self.thread_pool):
            self.thread_pool.cleanup()

        # cleaning up the reader thread
        self.debug("Cleaning the reader operations")
        if self.test(self.ctrl_reader, ReaderController):
            self.ctrl_reader.stopReader()
            self.ctrl_reader.cleanup()

        # cleaning up the writer thread
        self.debug("Cleaning the writer operations")
        if self.test(self.ctrl_writer):
            self.ctrl_writer.stopWriter()
            self.ctrl_writer.cleanup()

        # cleaning up the graph thread
        self.debug("Cleaning the graph operations")
        if self.test(self.ctrl_graph):
            self.ctrl_graph.stopGraph()
            self.ctrl_graph.cleanup()

        # restart program if requested
        app = QtGui.QApplication.instance()

        self.blockSignals(True)
        #for wdgt in app.topLevelWidgets():
        #    try:
        #        wdgt.close()
        #    except AttributeError:
        #        pass
        self.blockSignals(False)

        self.debug("Exiting the application ({})".format(QtGui.QApplication.topLevelWidgets()))
        
        if brestart:
            args = list(app.arguments())
            temp_app = args.pop(0)

            self.debug("Restarting the application ({}:{})".format(temp_app, args))
            QtCore.QProcess.startDetached(temp_app, args)

        # finish the application
        app.quit()

    def saveCurrentProfile(self):
        """
        Saves the currently selected profile as a pickle dump
        :return:
        """
        key = None
        filename = None
        try:
            key = PROFILE_START
            p = config.PROFILES[key]

            key = PROFILE_NICKNAME
            name = p[key]

            key = PROFILE_DIRSAVEDPROFILES
            prof_dir = config.PROFILES[key]

            data = deepcopy(config.PROFILES[PROFILE_START])

            # put empty space for the profile lambda reading configuration
            for (i, attr) in enumerate(data[PROFILE_TANGOATTR]):
                data[PROFILE_TANGOATTR][i][CMD] = None

            filename = self.PROFILE_PICKLE_TEMPLATE.format(name, time.strftime("%d-%b-%Y_%H-%M-%S", time.localtime()))
            pickle.dump(data, open(os.path.join(prof_dir, filename), "wb"))
        except AttributeError:
            self.debug("No profile was selected, exiting (error on key {})".format(key))

        return filename

    def restoreCurrentProfile(self):
        """
        Restore the values for the current profile from a pickled object
        :return:
        """
        self.debug("Tying to restore current profile information")
        d = QtCore.QDir(config.PROFILES[PROFILE_DIRSAVEDPROFILES])

        # setting filter
        filter = self.PROFILE_PICKLE_NAME_FILTER.format(config.PROFILES[PROFILE_START][PROFILE_NICKNAME])
        d.setNameFilters([filter])

        # setting sorting
        d.setSorting(QtCore.QDir.Time)

        elist = d.entryInfoList()

        # keep certain numbe rof configurations intact
        if len(elist)>self.PROFILES_MAX_NUMBER:
            prof2del = elist[-len(elist)+self.PROFILES_MAX_NUMBER-1:]

            for prof in prof2del:
                self.debug("Too many profiles, removing some ({})".format(prof.absoluteFilePath()))
                d.remove(prof.absoluteFilePath())

        # loading the latest profile info
        if len(elist)>0:
            self.restoreProfile(elist[0])

    def restoreProfile(self, fileinfo):
        """
        Restores a save profile
        :param filename:
        :return:
        """
        self.debug("Restoring a profile information from ({})".format(fileinfo.absoluteFilePath()))
        if fileinfo.isFile():
            data = pickle.load(open(str(fileinfo.absoluteFilePath()), "rb"))

            for key in data.keys():
                try:
                    if self.test(data[key]) and key!=PROFILE_TANGOATTR:
                        self.info("Loading the latest profile value ({}:{})".format(key, data[key]))
                        config.PROFILES[PROFILE_START][key] = deepcopy(data[key])
                    elif key == PROFILE_TANGOATTR:
                        # save command and assign it to the restored data
                        for (i, attr) in enumerate(data[PROFILE_TANGOATTR]):
                            cmd = config.PROFILES[PROFILE_START][PROFILE_TANGOATTR][i][CMD]
                            data[PROFILE_TANGOATTR][i][CMD] = cmd
                        config.PROFILES[PROFILE_START][PROFILE_TANGOATTR] = data[PROFILE_TANGOATTR]
                except AttributeError:
                    self.error("Error on loading a profile value (key: {})".format(key))
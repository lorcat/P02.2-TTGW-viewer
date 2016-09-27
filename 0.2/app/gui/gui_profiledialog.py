__author__ = 'lorcat'

import re
import imp
from PyQt4 import QtGui, QtCore

from app.gui.ui.ui_profiledialog import Ui_ProfileDialog
from app.common import Tester

from app.config.keys import *
from app.config import configuration as config


# class enabling profile selection
class ProfileDialog(QtGui.QDialog, Tester):
    # icon
    PROGRAM_ICON = 'program_icon.png'

    def __init__(self, parent=None):
        super(ProfileDialog, self).__init__(parent=parent)
        Tester.__init__(self)

        self.debug("Initialization")

        self.__init_variables()
        self.__init_ui()
        self.__init_events()

    def __init_variables(self):
        """
        Initializes variables used within the class and as output
        :return:
        """
        self.debug("Initialization of variables")

        self.__error = False

        # store profiles as (QFileInfo)
        self._profiles = []

        # gui
        self._ui = None

        # result - loaded module
        self._module = None

    @property
    def module(self):
        return self._module

    @property
    def error_state(self):
        return self.__error

    def __init_ui(self, path=None):
        """
        Initialization of the gui, fills elements with data
        :return:
        """
        self.debug("Initialization of UI")

        # path for the profiles
        path = config.PROFILES[PROFILE_DIR]
        self.debug("Profile path ({})".format(path))

        # make an icon
        image_path = self._provideImagePath()
        if image_path is not None:
            pixmap = QtGui.QPixmap(image_path.absoluteFilePath())
            self.setWindowIcon(QtGui.QIcon(pixmap))

        self._ui = Ui_ProfileDialog()
        self._ui.setupUi(self)

        dir = QtCore.QDir(path)

            # get iterator on files
        dirit = QtCore.QDirIterator(dir, QtCore.QDirIterator.NoIteratorFlags)

            # get string list to process profiles
        sl = QtCore.QStringList()

        # parse directory structure, find passing files profile*.py
        # get information from these files
        while dirit.hasNext():
            next = dirit.next()
            finfo = QtCore.QFileInfo(next)
            if finfo.isFile() and re.match(".*profile[^\\\/]*.py$", str(finfo.filePath()).lower()):
                mod = self._loadModule(finfo)
                if self.test(mod):
                    self.info("Found a profile ({})".format(finfo.absoluteFilePath()))
                    try:
                        sl.append(mod.START[PROFILE_NAME])
                    except KeyError:
                        sl.append(finfo.baseName())
                    self._profiles.append(finfo)

        if type(sl) is QtCore.QStringList:
            if len(sl):
                self._ui.lbPath.setText(dir.absolutePath())
                self._ui.lbPath.setToolTip("Path: {}".format(dir.absolutePath()))
                self._ui.lwFiles.insertItems(0, sl)
                self._ui.lwFiles.setCurrentRow(0)

    def __init_events(self):
        """
        Initialization of events working inside gui
        :return:
        """
        self.debug("Initialization of events")
        self.connect(self._ui.lwFiles, QtCore.SIGNAL("currentRowChanged(int)"), self.processProfileSelection)
        self.connect(self, QtCore.SIGNAL("finished(int)"), self.processExit)

    def processProfileSelection(self, index):
        """
        Processes selection of loaded module name
        :param index: int('index of self._profiles')
        :return:
        """
        self.debug("Processes profile selection by index ({})".format(index))

    def _loadModule(self, finfo):
        """
        Loads specific modules
        :param finfo: QFileInfo()
        :return: module('loaded')
        """
        self.debug("Loads a module based on QFileInfo ({})".format(finfo.absolutePath()))

        res = None
        name = str(finfo.baseName())

        fp = pathname = desc = None
        try:
            fp, pathname, desc =  imp.find_module(name, [str(finfo.absolutePath())])
        except ImportError:
            self.error("Error: cannot load profile '{}', please check path '{}'".format(name, finfo.absolutePath()))
            self.__error = True
            return

        if self.test(fp):
            try:
                res = imp.load_module(name, fp, pathname, desc)
            finally:
                if fp:
                    fp.close()
        return res

    def processExit(self, code):
        """
        Function to load specific module on exit
        :param code: int('index of profile to load')
        :return:
        """
        berror = False
        if self.test(code):
            index = int(self._ui.lwFiles.currentIndex().row())
            if index >-1:
                mod = self._loadModule(self._profiles[index])
                if self.test(mod):
                    self._module = mod
            else:
                berror = True
        else:
            berror = True

        if berror:
            self.error("No profile has been selected. Aborting..")
            QtGui.QApplication.instance().quit()

        self.deleteLater()

    def _provideImagePath(self):
        """
        Provides a reference to QFileInfo containing image file path for icon
        :param path: str()
        :return: None or QFileInfo()
        """
        res = None
        path = config.RESOURCES[RESOURCE_IMAGES]
        dir = QtCore.QDir(path)
        temp = QtCore.QFileInfo()
        temp.setFile(dir, self.PROGRAM_ICON)
        if temp.isFile():
            res = temp
        else:
            self.error("{}. No image file is present at the path ({})".format(self.__class__.__name__, path))
        return res

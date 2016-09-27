__author__ = 'glazyrin'

from app.common import *
from app.config import configuration as config
from app.gui.ui.ui_roi import Ui_Form

class RoiUpdater(QtGui.QWidget, Tester, Ui_Form):

    sign_updateframe = QtCore.pyqtSignal(object, object)

    def __init__(self, parent=None, starter=None):
        Tester.__init__(self)
        QtGui.QWidget.__init__(self, parent=parent)

        # reference to the starter
        self.starter = starter

        # setup ui
        self.setupUi(self)

        # initialize events
        self.initEvents()

    def initEvents(self):
        """
        Initializes events for the ROI menu class
        :return:
        """
        self.debug("Initializing events")

        self.connect(self.btn_roisync, QtCore.SIGNAL("clicked()"), self.updateRoiInfo)
        self.connect(self.btn_roiapply, QtCore.SIGNAL("clicked()"), self.applyRoi)

        self.sign_updateframe.connect(self.starter.ctrl_reader.repeatLastFrame)

    def showEvent(self, event):
        """
        Actions to process on the show event
        :param QHideEvent:
        :return:
        """
        self.debug("Performing actions on the show event")

        # silently update info on the current roi
        self.updateRoiInfo(skiperror=True)

    def updateRoiInfo(self, skiperror=False):
        """
        Updates information on the current roi
        :param skiperror:
        :return:
        """
        self.debug("Trying to update information on the rois (skip errors: {})".format(skiperror))

        view_data = self.starter._mainwnd.view_data
        view_channel = self.starter._mainwnd.view_channel

        if self.test(view_data) and self.test(view_channel):
            data = view_data[view_channel]

            wdgts = (self.dsb_roix, self.dsb_roiy, self.dsb_roiw, self.dsb_roih)
            for (i, wdgt) in enumerate(wdgts):
                try:
                    wdgt.setValue(int(data[ROI_VIEW][i]))
                except ValueError:
                    self.error("Roi element number ({}) is not a int".format(i))
        elif not skiperror:
            QtGui.QMessageBox.warning(self.starter._mainwnd, "Error", "Please start viewer and get an image first", QtGui.QMessageBox.Ok)

    def applyRoi(self):
        """
        Updates information on the current roi to the gui
        :param skiperror:
        :return:
        """
        self.debug("Trying to update information on the rois with the profile")

        view_data = self.starter._mainwnd.view_data
        view_channel = self.starter._mainwnd.view_channel

        if self.test(view_data) and self.test(view_channel):
            roi = []

            wdgts = (self.dsb_roix, self.dsb_roiy, self.dsb_roiw, self.dsb_roih)
            for (i, wdgt) in enumerate(wdgts):
                try:
                    roi.append(int(wdgt.value()))
                except ValueError:
                    self.error("Roi element number ({}) is not a float".format(i))

            # find proper channel
            nick = None
            for (i, el) in enumerate(config.PROFILES[PROFILE_START][PROFILE_TANGOATTR]):
                if view_data[view_channel][NICK] == el[NICK]:
                    array = el[ROI_VIEW]
                    config.PROFILES[PROFILE_START][PROFILE_TANGOATTR][i][ROI_VIEW] = roi
                    del array[:]
                    nick = el[NICK]
                    break

            if self.test(nick):
                # update last roi frame
                self.sign_updateframe.emit(nick, roi)
        else:
            QtGui.QMessageBox.warning(self.starter._mainwnd, "Error", "Please start viewer and get an image first", QtGui.QMessageBox.Ok)
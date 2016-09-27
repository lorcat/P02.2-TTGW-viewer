__author__ = 'Konstantin Glazyrin'

from copy import deepcopy

from app.config import configuration as config
from app.common import *
from app.gui.ui.ui_mainwindow import *
from app.gui.gui_roi import RoiUpdater

import numpy

class MainWindow(QtGui.QMainWindow, Ui_MainWindow, Tester):

    # window status bar message delay
    DEFAULT_STATUSDELAY = 5000

    sign_updatestats = QtCore.pyqtSignal(object)

    # MENU names
    MENU_CONTROLLERS = "&Controllers"

    # title for a dialog saving profiles
    PROFILE_SAVE_DIALOG_TITLE = "Saving profile"

    def __init__(self, parent=None, starter=None):
        Tester.__init__(self)
        QtGui.QMainWindow.__init__(self, parent=parent)

        # thread pool
        self.thread_pool = get_threadpool(parent=self)

        # starter - object with references to the reader and the writer
        self.starter = starter

        # Scene object
        self.scene = None

        # rois to control view and fit
        self.roi_view = None

        #  flags controlling auto parameters of the pyqtgraph ImageView
        self.auto_range = True
        self.auto_levels = True
        self.auto_hist_range = True

        # pixmap object
        self.pixmap = None

        # channel mode - many images, each is a channel
        self.view_channel = 0
        self.max_view_channels = 0
        # last copy of data
        self.view_data = None
        self.view_nick = None

        # counter for the bad frames
        self.bad_frame = 0

        # center of mass objects - dynamically updated crosses
        self.coms = []

        # roiaction - menuitem for ROI control
        self.roiactwdgt = None

        self.initGui()
        self.initEvents()
        self.initializeMenu()
        self.initIcon()

        self.show()

    def initGui(self):
        """
        Initializes GUI
        :return:
        """
        self.debug("Initializing gui of the main window")
        self.setupUi(self)

        self.setWindowTitle(config.MAIN_WINDOW[WINDOW_TITLE])

        # hide unnecessary buttons for the ImageView
        self.resetImageViewGui()

        # example of the image elements
        self.scene = self.gv_main.scene

        # set roi for the enhanced view and for the fit
        self.roi_view = QtGui.QGraphicsRectItem(scene=self.scene)
        self.roi_view.setParentItem(self.gv_main.getImageItem())

        # side image with zoomed in view
        self.sideimage_view = QtGui.QGraphicsRectItem(scene=self.scene)

        # load an image with rect
        self.sideimage = pg.ImageItem(np.arange(100).reshape(10, 10).astype(np.float32))
        self.sideimage.setRect(QtCore.QRectF(*config.PROFILES[PROFILE_START][PROFILE_INSERT_RECT]))

        brush = QtGui.QBrush(QtGui.QColor(*config.PROFILES[PROFILE_START][PROFILE_INSERTVIEW_LINES][0]))
        pw = config.PROFILES[PROFILE_START][PROFILE_INSERTVIEW_LINES][1]
        ps = pw = config.PROFILES[PROFILE_START][PROFILE_INSERTVIEW_LINES][2]
        self.vline = QtGui.QGraphicsLineItem(scene=self.scene, parent=self.sideimage)
        self.vline.setPen(QtGui.QPen(brush, pw, ps))
        self.hline = QtGui.QGraphicsLineItem(scene=self.scene, parent=self.sideimage)
        self.hline.setPen(QtGui.QPen(brush, pw, ps))

        # self.sideimage.setParentItem(self.sideimage_view)
        self.scene.addItem(self.sideimage)

        # update lookup tables
        self.gv_main.ui.histogram.gradient.loadPreset(config.PROFILES[PROFILE_START][PROFILE_COLORTABLE])

        # menu elements
        self.actShowViewROI.setChecked(config.PROFILES[PROFILE_START][PROFILE_SHOW_ROIVIEW])

    def initEvents(self):
        """
        Initializes event for buttons and other things
        :return:
        """
        self.debug("Initializing events for the main window children")

        # disable reader on start
        self.readerStartStop(False, init=True)
        self.connect(self.btn_readerStartStop, QtCore.SIGNAL("toggled(bool)"), self.readerStartStop)
        self.connect(self.actShowViewROI, QtCore.SIGNAL("triggered(bool)"), self.viewRoiShowHide)
        self.connect(self.actSaveImage, QtCore.SIGNAL("triggered(bool)"), self.makeReport)
        # for updates of the stat object
        self.registerUpdateStats(self.updateStats)

        # save and load profile state
        self.connect(self.actSaveState, QtCore.SIGNAL("triggered()"), self.saveProfileState)
        self.connect(self.actLoadState, QtCore.SIGNAL("triggered()"), self.loadProfileState)

        # image view
        self.gv_main.scene.sigMouseMoved.connect(self.trackImageViewMouse)
        self.gv_main.ui.histogram.sigLookupTableChanged.connect(self.updateLookupTable)

        self.gv_main.ui.histogram.sigLevelsChanged.connect(self.updateLevels)

    def readerStartStop(self, bstart, init=False):
        """
        Function processes reader controller actions - start/stop
        :param baction: flag representing state
        :return:
        """
        self.debug("Processing start/stop reader action")
        str_start = "Start"
        str_stop = "Stop"

        action = self.actReaderStartStop
        btn = self.btn_readerStartStop

        # start or stop reader
        action.blockSignals(True)
        if bstart:
            action.setText(str_stop)
            btn.setText(str_stop)
            if self.test(self.starter.ctrl_reader) and not init:
                self.starter.ctrl_reader.startReader()
        else:
            action.setText(str_start)
            btn.setText(str_start)
            if self.test(self.starter.ctrl_reader) and not init:
                self.starter.ctrl_reader.stopReader()
        action.blockSignals(False)

    def viewRoiShowHide(self, bshow):
        """
        Function processes actions with view roi visibility
        :param bshow: flag representing state
        :return:
        """
        self.debug("Processing show/hide view ROI action")
        action = self.actShowViewROI

        # start or stop reader
        action.blockSignals(True)
        config.PROFILES[PROFILE_START][PROFILE_SHOW_ROIVIEW] = bshow
        self.updateView()
        action.blockSignals(False)

    def getUpdatedGraph(self, data):
        """
        Retrieves the prepared images and displays it in the graphics scene
        :return:
        """
        self.debug("Displaying the prepared images ({})".format(data))

        # make a copy to release memory faster
        self.view_data = deepcopy(data)

        # update graph - show channel
        self.updateView()

    def updateView(self, bupdate_graph = True):
        """
        Shows the selected data channel
        :return:
        """
        # updating the image

        # current view
        view = None

        # select channel

        chcount = 0
        for (i, el) in enumerate(self.view_data):
            if self.test(el[DATA], np.ndarray):
                if chcount == self.view_channel:
                    view = el
                chcount += 1
        self.max_view_channels = chcount

        if self.max_view_channels == 0:
            self.error("No Image provided")
            self.bad_frame += 1
            return

        # if there is a change in image number - change the selected channel
        if self.max_view_channels <= self.view_channel:
            self.view_channel = 0

        # default image
        image = np.arange(100).reshape(10,10)
        thumbview = np.arange(100).reshape(10,10)

        nick = "Empty"
        try:
            if self.test(view):
                image = view[DATA]

                if config.PROFILES[PROFILE_START][PROFILE_SHOW_ROIVIEW]:
                    thumbview = view[ROI_VIEWDATA]
                else:
                    thumbview = view[ROI_FITDATA]

                # get information on the current channel
                roi_fit = view[ROI_VIEW]
                roi_view = view[ROI_VIEW]
                penfit = view[PENFIT]
                penview = view[PENVIEW]
                self.view_nick = view[NICK]

                self.roi_view.setPen(QtGui.QPen(QtGui.QBrush(penview[0]), penview[1], style=penview[2]))

                # always show roi view
                self.roi_view.setParentItem(self.gv_main.getImageItem())
                x,y,w,h = roi_view
                self.roi_view.setRect( y, x, w, h)

                # updating center of the view image
                br = self.sideimage.boundingRect()
                x, y, w, h = br.x()+br.width()/2, 0, br.x()+br.width()/2, br.height()
                self.vline.setLine(x, y, w, h)

                x, y, w, h = 0, br.y() + br.height() / 2, br.width(), br.y() + br.height() / 2
                self.hline.setLine(x, y, w, h)

                # work with center of mass
                # cleanup existing labels for the center of mass
                while len(self.coms)>0:
                    com = self.coms.pop(-1)
                    self.scene.removeItem(com)

                # if we have information on the center of mass - let's show cross there and report the stats
                if len(view[ROI_FITCOMS]) > 0:
                    for (i, com) in enumerate(view[ROI_FITCOMS]):
                        style = config.PROFILES[PROFILE_START][PROFILE_INSERTCENTER_LINES]

                        oh = QtGui.QGraphicsLineItem(scene=self.scene)
                        oh.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(*style[0])), style[1]))

                        ov = QtGui.QGraphicsLineItem(scene=self.scene)
                        ov.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(*style[0])), style[1]))

                        oh.setParentItem(self.sideimage)
                        ov.setParentItem(self.sideimage)

                        self.coms.append(oh)
                        self.coms.append(ov)

                        fwhmx = view[ROI_FITFWHMX][i]
                        fwhmy = view[ROI_FITFWHMY][i]

                        # object with statistics passed to the gui
                        stat_obj = {CENTER: "{}:{}".format(com[1]+view[ROI_VIEW][1], com[0]+view[ROI_VIEW][0]),
                                    FWHMX: fwhmy, FWHMY: fwhmx}

                        self.reportUpdateStats(stat_obj)

                        x1, x2, y1, y2 = com[0]-fwhmx/4, com[0]+fwhmx/4, com[1], com[1]
                        oh.setLine(x1, y1, x2, y2)

                        x1, x2, y1, y2 = com[0], com[0], com[1]  - fwhmy / 4, com[1] + fwhmy / 4
                        ov.setLine(x1, y1, x2, y2)
                        self.coms.append(oh)
                        ov.update()
                        oh.update()

            else:
                raise ValueError
        except (KeyError, ValueError):
            self.error("No image is provided, using the default one")

        if bupdate_graph:
            try:
                self.gv_main.setImage(image, autoRange=self.auto_range, autoLevels=self.auto_levels, autoHistogramRange=self.auto_hist_range)
                self.sideimage.setImage(thumbview)
            except TypeError:
                self.error("Bad Frame")
                self.bad_frame += 1

        # reset auto parameters to keep with user settings
        self.resetImageViewParams()

        # updates image levels in case we need this - only for ROI_VIEW
        if config.PROFILES[PROFILE_START][PROFILE_SHOW_ROIVIEW]:
            self.updateLevels()

        self.gv_main.update()

    def resetImageViewParams(self):
        """
        Resets the auto parameters with respect to the ImageView
        :return:
        """
        self.auto_range = False
        self.auto_levels = False
        self.auto_hist_range = False

    def resetImageViewGui(self):
        """
        Disables certain graphic parameters for the image view
        :return:
        """
        try:
            self.gv_main.ui.roiBtn.hide()
        except AttributeError:
            self.error("Problem with pyqtgraph ImageView gui elements (roi)")

        try:
            self.gv_main.ui.menuBtn.hide()
        except AttributeError:
            self.error("Problem with pyqtgraph ImageView gui elements (menu)")

        try:
            self.gv_main.ui.normBtn.hide()
        except AttributeError:
            self.error("Problem with pyqtgraph ImageView gui elements (norm)")

    def trackImageViewMouse(self, view_pos):
        """
        Function tracking mouse position
        :return:
        """
        # self.debug("Tracking mouse position ({})".format(view_pos))
        if self.test(self.gv_main.image):
            data = self.gv_main.image
            nr, nc = data.shape
            scpos = self.gv_main.getImageItem().mapFromScene(view_pos)

            row, col = int(scpos.y()), int(scpos.x())

            if (0 <= row <= nr) and (0 <= col <= nc):
                self.reportStatus("X: {}; Y: {}".format(col, row))
            else:
                pass

    def reportStatus(self, msg):
        """
        Shows a message in the status bar
        :param msg:
        :return:
        """
        self.debug("Showing status message ({})".format(msg))
        sb = self.statusBar()
        sb.showMessage(str(msg), self.DEFAULT_STATUSDELAY)

    def updateLookupTable(self, hist):
        """
        Processes changes of the lookup table
        :return:
        """
        self.debug("Detecting a change of the histogram ({})".format(hist))
        self.debug(hist.getLookupTable(n=512))

        self.sideimage.setLookupTable(hist.getLookupTable(n=512), update=True)

    def updateLevels(self):
        """
            Processes changes of the levels
            :return:
        """
        self.debug("Detecting a change of the levels")

        self.sideimage.setLevels(self.gv_main.ui.histogram.region.getRegion())
        self.sideimage.update()

    def closeEvent(self, event):
        """
        Cleaning up gui elements
        :param event:
        :return:
        """
        self.debug("Cleaning upd gui elements")
        self.gv_main.close()

        # cleanup the procedure
        self.starter.cleanup()

    def registerUpdateStats(self, func):
        """
        Registers a function to be fired on fit stats update
        :return:
        """
        self.debug("Registering function for sing-updatestats")
        self.sign_updatestats.connect(func)

    def reportUpdateStats(self, stat_obj):
        """
        Reporting updates statistics
        :return:
        """
        self.debug("Reporting updated statistics of the fit ({})".format(stat_obj))
        self.sign_updatestats.emit(deepcopy(stat_obj))

    def updateStats(self, stat_obj):
        """
        Updating the fit statistics
        :param stat_obj:
        :return:
        """
        self.debug("Updating the statistics")

        if self.test(stat_obj):
            self.lbl_center.setText(str(stat_obj[CENTER]))
            self.lbl_fwhmx.setText(str(stat_obj[FWHMY]))
            self.lbl_fwhmy.setText(str(stat_obj[FWHMX]))

    def processControllersMenu(self, action):
        """
        Processes actions with controller menu
        :param action:
        :return:
        """
        self.debug("Processing controller menu action ({})".format(action))
        for (i, act) in enumerate(self.ctrl_menu.actions()):
            if act == action:
                self.debug("Action is found")
                try:
                    key = CMD
                    cmd_name = config.PROFILES[PROFILE_START][PROFILE_CONTROLLERS][i][key]
                    key = ARGS
                    cmd_args = config.PROFILES[PROFILE_START][PROFILE_CONTROLLERS][i][key]

                    runner = ProcessRunner(cmd_name, cmd_args)
                    self.thread_pool.tryStart(runner)
                except KeyError:
                    self.error("Configuration error; key ({}) does not exist..".format(key))

                break

    def initializeMenu(self):
        """
        Initializes main program menu
        :return:
        """
        self.debug("Adding application menus")
        mb = self.menuBar()

        # adding menu with controllers - executables to run
        self.ctrl_menu = mb.addMenu(self.MENU_CONTROLLERS)
        for (i, el) in enumerate(config.PROFILES[PROFILE_START][PROFILE_CONTROLLERS]):
            try:
                key = CMD
                if el[key] != SEPARATOR:
                    key = NICK
                    self.debug("Adding action ({}:{})".format(key, el[key]))
                    act = QtGui.QAction(el[key], self.ctrl_menu)
                    self.ctrl_menu.addAction(act)
                else:
                    self.debug("Adding separator")
                    self.ctrl_menu.addSeparator()
            except KeyError:
                self.error(
                    "Configuration error; key ({}) does not exist, skipping controller..".format(key))
                continue

        # initialize menu for ROI updating
        self.roiactwdgt = QtGui.QWidgetAction(self.menuROI)
        w = RoiUpdater(parent=self.menuROI, starter=self.starter)
        self.roiactwdgt.setDefaultWidget(w)
        self.menuROI.addAction(self.roiactwdgt)

        # initialize events for controllers
        self.connect(self.ctrl_menu, QtCore.SIGNAL("triggered(QAction*)"), self.processControllersMenu)

    def makeReport(self):
        """
        Function preparing a report to be sent our
        :return:
        """
        self.debug("Preparing a report")
        img = self.gv_main.getImageItem()

        if self.test(self.view_data):
            exporter = pyqtgraph.exporters.ImageExporter(self.gv_main.getImageItem())
            # saving image
            loctime = time.localtime()
            filename = "report_{}-{}.png".format(self.view_data[self.view_channel][NICK], time.strftime("%d-%b-%Y_%H-%M-%S", loctime))
            fnimage = os.path.join(config.PROFILES[PROFILE_DIRREPORTS], filename)
            self.debug("Filename is ({})".format(fnimage))
            exporter.export(fnimage)

            # quickly save file with fit parameters
            filename = "report_{}-{}.txt".format(self.view_data[self.view_channel][NICK], time.strftime("%d-%b-%Y_%H-%M-%S", loctime))
            fntext = os.path.join(config.PROFILES[PROFILE_DIRREPORTS], filename)
            file = open(fntext, "w")

            file.write("""Report on beamposition; CENTER: {};  FWHMX: {}; FWHMY: {}\n""".format(self.lbl_center.text(), self.lbl_fwhmy.text(), self.lbl_fwhmx.text()))
            file.close()

            QtGui.QMessageBox.information(self, "File saved", "The files were saved under:\n{}\n{}".format(fnimage, fntext))
        else:
            QtGui.QMessageBox.critical(self,"Error", "No image is available - please load it first")

    def initIcon(self):
        """
        Sets the icon for the window
        :return:
        """
        self.debug("Preparing window icon")

        path = config.RESOURCES[RESOURCE_IMAGES]
        self.debug("Preparing image path, directory ({})".format(path))

        res = None
        dir = QtCore.QDir(path)
        temp = QtCore.QFileInfo()
        temp.setFile(dir, 'program_icon.png')
        if temp.isFile():
            self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(temp.absoluteFilePath())))

        return res

    def saveProfileState(self):
        """
        Saves the state of the profile as a pickle
        :return:
        """
        filename = self.starter.saveCurrentProfile()
        QtGui.QMessageBox.information(self, "File saved", "File saved as:\n{}".format(filename))

    def loadProfileState(self):
        """
        Loads a profile state saved as a pickle the state of the profile as a pickle
        :return:
        """
        self.debug("Starting dialog for filename selection")

        # gets filename until a correct one is selected
        filter = self.starter.PROFILE_PICKLE_TEMPLATE.format(config.PROFILES[PROFILE_START][PROFILE_NICKNAME], "*")
        print filter

        filename = QtGui.QFileDialog.getOpenFileName(parent=self, caption=self.PROFILE_SAVE_DIALOG_TITLE,
                                                     directory=config.PROFILES[PROFILE_DIRSAVEDPROFILES], filter=filter, selectedFilter=filter)

        if self.test(filename) and len(filename) > 0:
            fileinfo = QtCore.QFileInfo(filename)
            if fileinfo.isFile():
                self.starter.restoreProfile(fileinfo)
                QtGui.QMessageBox.information(self, "Profile restored", "Successfully restored profile:\n{}".format(fileinfo.absoluteFilePath()))
            else:
                QtGui.QMessageBox.critical(self, "Profile restoration failed",
                                      "Could not restore profile:\n{}".format(fileinfo.absoluteFilePath()))
        return

# @TODO: movement of the image insert
# @TODO: report sending
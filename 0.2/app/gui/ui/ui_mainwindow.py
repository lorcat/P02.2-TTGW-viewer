# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(911, 686)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/buttons/images/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setStyleSheet(_fromUtf8("QLabel {font-family: Arial; font-size: 10pt;}\n"
"QStatusBar(background-color:#fff;)"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet(_fromUtf8("QWidget {background: #fff;}\n"
"\n"
"*[class~=\"QPushButton\"] {border:0px; padding: 5px; padding-left:10px; padding-right: 10px;}\n"
"*[class~=\"QPushButton\"]:hover {background-color: #eee; color: #000;}\n"
"*[class~=\"QPushButton\"]:pressed {background-color:#ecc}\n"
"\n"
"*[class~=\"QSpinBox\"] {border: 2px solid #ccc;}\n"
"*[class~=\"QSpinBox\"]:hover {border: 2px solid #ecc;}\n"
"\n"
"*[class~=\"QSpinBox\"]::up-button {subcontrol-origin: border;\n"
"    subcontrol-position: top right; \n"
"    width: 20px; \n"
"    border-image: url(:/buttons/images/spinup.png) 0.5;\n"
"    border-width: 1px;}\n"
"*[class~=\"QSpinBox\"]::up-button:pressed {background-color: #ecc;}\n"
"*[class~=\"QSpinBox\"]::up-button:hover {background-color: #eee;}\n"
"\n"
"*[class~=\"QSpinBox\"]::down-button {subcontrol-origin: border;\n"
"    subcontrol-position: bottom right; \n"
"    width: 20px; \n"
"    border-image: url(:/buttons/images/spindown.png) 0.5;\n"
"    border-width: 1px;}\n"
"*[class~=\"QSpinBox\"]::down-button:pressed {background-color: #ecc;}\n"
"*[class~=\"QSpinBox\"]::down-button:hover {background-color: #eee;}\n"
"\n"
"*[class~=\"QGraphicsView\"]::down-button:hover {border: 0px solid #000;}\n"
"\n"
"*[class~=\"QLabel\"]#lbl_center {font-weight:bold; color: #a00;}\n"
"*[class~=\"QLabel\"]#lbl_fwhmx {font-weight:bold; color: #a00;}\n"
"*[class~=\"QLabel\"]#lbl_fwhmy {font-weight:bold; color: #a00;}"))
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.wupper = QtGui.QWidget(self.centralwidget)
        self.wupper.setMaximumSize(QtCore.QSize(16777215, 50))
        self.wupper.setObjectName(_fromUtf8("wupper"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.wupper)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(self.wupper)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.btn_readerStartStop = QtGui.QPushButton(self.wupper)
        self.btn_readerStartStop.setCheckable(True)
        self.btn_readerStartStop.setChecked(False)
        self.btn_readerStartStop.setObjectName(_fromUtf8("btn_readerStartStop"))
        self.horizontalLayout.addWidget(self.btn_readerStartStop)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(self.wupper)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lbl_center = QtGui.QLabel(self.wupper)
        self.lbl_center.setMinimumSize(QtCore.QSize(150, 0))
        self.lbl_center.setText(_fromUtf8(""))
        self.lbl_center.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_center.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.lbl_center.setObjectName(_fromUtf8("lbl_center"))
        self.horizontalLayout.addWidget(self.lbl_center)
        self.label_4 = QtGui.QLabel(self.wupper)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.lbl_fwhmx = QtGui.QLabel(self.wupper)
        self.lbl_fwhmx.setMinimumSize(QtCore.QSize(75, 0))
        self.lbl_fwhmx.setText(_fromUtf8(""))
        self.lbl_fwhmx.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_fwhmx.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.lbl_fwhmx.setObjectName(_fromUtf8("lbl_fwhmx"))
        self.horizontalLayout.addWidget(self.lbl_fwhmx)
        self.label_6 = QtGui.QLabel(self.wupper)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.lbl_fwhmy = QtGui.QLabel(self.wupper)
        self.lbl_fwhmy.setMinimumSize(QtCore.QSize(75, 0))
        self.lbl_fwhmy.setText(_fromUtf8(""))
        self.lbl_fwhmy.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_fwhmy.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse|QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.lbl_fwhmy.setObjectName(_fromUtf8("lbl_fwhmy"))
        self.horizontalLayout.addWidget(self.lbl_fwhmy)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addWidget(self.wupper, 0, 0, 1, 1)
        self.gv_main = ImageView(self.centralwidget)
        self.gv_main.setStyleSheet(_fromUtf8(""))
        #self.gv_main.setFrameShape(QtGui.QFrame.NoFrame)
        self.gv_main.setObjectName(_fromUtf8("gv_main"))
        self.gridLayout.addWidget(self.gv_main, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 911, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuReport = QtGui.QMenu(self.menubar)
        self.menuReport.setObjectName(_fromUtf8("menuReport"))
        self.menuProfile = QtGui.QMenu(self.menubar)
        self.menuProfile.setObjectName(_fromUtf8("menuProfile"))
        self.menuROI = QtGui.QMenu(self.menubar)
        self.menuROI.setObjectName(_fromUtf8("menuROI"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setStyleSheet(_fromUtf8("QStatusBar {background-color: #fff;}"))
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actReaderStartStop = QtGui.QAction(MainWindow)
        self.actReaderStartStop.setCheckable(True)
        self.actReaderStartStop.setObjectName(_fromUtf8("actReaderStartStop"))
        self.actReaderStop = QtGui.QAction(MainWindow)
        self.actReaderStop.setObjectName(_fromUtf8("actReaderStop"))
        self.actShowViewROI = QtGui.QAction(MainWindow)
        self.actShowViewROI.setCheckable(True)
        self.actShowViewROI.setObjectName(_fromUtf8("actShowViewROI"))
        self.actShowFitROI = QtGui.QAction(MainWindow)
        self.actShowFitROI.setCheckable(True)
        self.actShowFitROI.setObjectName(_fromUtf8("actShowFitROI"))
        self.actSaveImage = QtGui.QAction(MainWindow)
        self.actSaveImage.setObjectName(_fromUtf8("actSaveImage"))
        self.actLoadState = QtGui.QAction(MainWindow)
        self.actLoadState.setObjectName(_fromUtf8("actLoadState"))
        self.actSaveState = QtGui.QAction(MainWindow)
        self.actSaveState.setObjectName(_fromUtf8("actSaveState"))
        self.menuView.addAction(self.actShowViewROI)
        self.menuReport.addAction(self.actSaveImage)
        self.menuProfile.addAction(self.actLoadState)
        self.menuProfile.addAction(self.actSaveState)
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuReport.menuAction())
        self.menubar.addAction(self.menuProfile.menuAction())
        self.menubar.addAction(self.menuROI.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Reader:", None))
        self.btn_readerStartStop.setText(_translate("MainWindow", "Start/Stop", None))
        self.label_2.setText(_translate("MainWindow", "Center:", None))
        self.label_4.setText(_translate("MainWindow", "FWHMx:", None))
        self.label_6.setText(_translate("MainWindow", "FWHMy:", None))
        self.menuView.setTitle(_translate("MainWindow", "View", None))
        self.menuReport.setTitle(_translate("MainWindow", "Report", None))
        self.menuProfile.setTitle(_translate("MainWindow", "Profile", None))
        self.menuROI.setTitle(_translate("MainWindow", "ROI", None))
        self.actReaderStartStop.setText(_translate("MainWindow", "Start", None))
        self.actReaderStop.setText(_translate("MainWindow", "Stop", None))
        self.actShowViewROI.setText(_translate("MainWindow", "Show View ROI", None))
        self.actShowFitROI.setText(_translate("MainWindow", "Show Fit ROI", None))
        self.actSaveImage.setText(_translate("MainWindow", "Save Image", None))
        self.actLoadState.setText(_translate("MainWindow", "Load State", None))
        self.actSaveState.setText(_translate("MainWindow", "Save State", None))

from pyqtgraph import ImageView

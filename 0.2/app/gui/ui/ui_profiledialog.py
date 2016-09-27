# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_profiledialog.ui'
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

class Ui_ProfileDialog(object):
    def setupUi(self, ProfileDialog):
        ProfileDialog.setObjectName(_fromUtf8("ProfileDialog"))
        ProfileDialog.resize(508, 436)
        self.layoutWidget = QtGui.QWidget(ProfileDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 11, 481, 411))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lbPath = QtGui.QLabel(self.layoutWidget)
        self.lbPath.setMinimumSize(QtCore.QSize(0, 30))
        self.lbPath.setText(_fromUtf8(""))
        self.lbPath.setObjectName(_fromUtf8("lbPath"))
        self.gridLayout.addWidget(self.lbPath, 0, 1, 1, 1)
        self.lwFiles = QtGui.QListWidget(self.layoutWidget)
        self.lwFiles.setObjectName(_fromUtf8("lwFiles"))
        self.gridLayout.addWidget(self.lwFiles, 1, 0, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(self.layoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.gridLayout.setRowStretch(1, 50)

        self.retranslateUi(ProfileDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ProfileDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ProfileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProfileDialog)

    def retranslateUi(self, ProfileDialog):
        ProfileDialog.setWindowTitle(_translate("ProfileDialog", "Please Select Profile", None))
        self.label.setText(_translate("ProfileDialog", "Path:", None))
        self.lwFiles.setToolTip(_translate("ProfileDialog", "List of profiles with different motor sets", None))


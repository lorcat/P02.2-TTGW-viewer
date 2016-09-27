# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_roi.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(388, 88)
        Form.setStyleSheet(_fromUtf8("QWidget {background: #fff;}\n"
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
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.widget = QtGui.QWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 0, 3, 1, 1)
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 1, 3, 1, 1)
        self.label_2 = QtGui.QLabel(self.widget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.dsb_roih = QtGui.QDoubleSpinBox(self.widget)
        self.dsb_roih.setMinimumSize(QtCore.QSize(75, 30))
        self.dsb_roih.setDecimals(0)
        self.dsb_roih.setMinimum(0.0)
        self.dsb_roih.setMaximum(3000.0)
        self.dsb_roih.setProperty("value", 0.0)
        self.dsb_roih.setObjectName(_fromUtf8("dsb_roih"))
        self.gridLayout_2.addWidget(self.dsb_roih, 1, 4, 1, 1)
        self.dsb_roiw = QtGui.QDoubleSpinBox(self.widget)
        self.dsb_roiw.setMinimumSize(QtCore.QSize(75, 30))
        self.dsb_roiw.setDecimals(0)
        self.dsb_roiw.setMinimum(0.0)
        self.dsb_roiw.setMaximum(1000.0)
        self.dsb_roiw.setProperty("value", 0.0)
        self.dsb_roiw.setObjectName(_fromUtf8("dsb_roiw"))
        self.gridLayout_2.addWidget(self.dsb_roiw, 0, 4, 1, 1)
        self.btn_roiapply = QtGui.QPushButton(self.widget)
        self.btn_roiapply.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_roiapply.setObjectName(_fromUtf8("btn_roiapply"))
        self.gridLayout_2.addWidget(self.btn_roiapply, 0, 7, 2, 1)
        self.btn_roisync = QtGui.QPushButton(self.widget)
        self.btn_roisync.setMinimumSize(QtCore.QSize(0, 40))
        self.btn_roisync.setObjectName(_fromUtf8("btn_roisync"))
        self.gridLayout_2.addWidget(self.btn_roisync, 0, 6, 2, 1)
        self.dsb_roix = QtGui.QDoubleSpinBox(self.widget)
        self.dsb_roix.setMinimumSize(QtCore.QSize(75, 30))
        self.dsb_roix.setDecimals(0)
        self.dsb_roix.setMinimum(0.0)
        self.dsb_roix.setMaximum(3000.0)
        self.dsb_roix.setProperty("value", 0.0)
        self.dsb_roix.setObjectName(_fromUtf8("dsb_roix"))
        self.gridLayout_2.addWidget(self.dsb_roix, 1, 1, 1, 1)
        self.dsb_roiy = QtGui.QDoubleSpinBox(self.widget)
        self.dsb_roiy.setMinimumSize(QtCore.QSize(75, 30))
        self.dsb_roiy.setDecimals(0)
        self.dsb_roiy.setMinimum(0.0)
        self.dsb_roiy.setMaximum(3000.0)
        self.dsb_roiy.setProperty("value", 0.0)
        self.dsb_roiy.setObjectName(_fromUtf8("dsb_roiy"))
        self.gridLayout_2.addWidget(self.dsb_roiy, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.dsb_roiw, self.dsb_roih)
        Form.setTabOrder(self.dsb_roih, self.btn_roisync)
        Form.setTabOrder(self.btn_roisync, self.btn_roiapply)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_3.setText(_translate("Form", "ROI W:", None))
        self.label.setText(_translate("Form", "ROI X:", None))
        self.label_4.setText(_translate("Form", "ROI H:", None))
        self.label_2.setText(_translate("Form", "ROI Y:", None))
        self.dsb_roih.setSuffix(_translate("Form", " px", None))
        self.dsb_roiw.setSuffix(_translate("Form", " px", None))
        self.btn_roiapply.setText(_translate("Form", "Apply", None))
        self.btn_roisync.setText(_translate("Form", "Sync", None))
        self.dsb_roix.setSuffix(_translate("Form", " px", None))
        self.dsb_roiy.setSuffix(_translate("Form", " px", None))


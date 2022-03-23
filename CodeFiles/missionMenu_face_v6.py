# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'missionMenu.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_missionMenu(object):
    def setupUi(self, missionMenu):
        missionMenu.setObjectName("missionMenu")
        missionMenu.setEnabled(True)
        missionMenu.resize(450, 370)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(missionMenu.sizePolicy().hasHeightForWidth())
        missionMenu.setSizePolicy(sizePolicy)
        missionMenu.setMaximumSize(QtCore.QSize(450, 370))
        missionMenu.setStyleSheet("")
        self.comboBox = QtWidgets.QComboBox(missionMenu)
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 231, 61))
        font = QtGui.QFont()
        font.setFamily("Montserrat")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0284091, x2:0.836, y2:0.0336818, stop:0 rgba(0, 198, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
"\n"
"color: rgb(255, 255, 255);\n"
"border: 2px solid;\n"
"border-color: rgb(255, 255, 255);\n"
"border-radius:10px;\n"
"padding-left:30px;\n"
"padding-bottom:8px;\n"
"\n"
"")
        self.comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtCurrent)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.applyLabel = QtWidgets.QLabel(missionMenu)
        self.applyLabel.setGeometry(QtCore.QRect(10, 100, 111, 41))
        self.applyLabel.setStyleSheet("QLabel{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.502, y2:0.517091, stop:0 rgba(36, 225, 42, 255), stop:1 rgba(13, 110, 8, 255));\n"
"  width: 100%;\n"
"  z-index: -1;\n"
"  position: relative;\n"
"  height: 100%;\n"
"  top: 7px;\n"
"  left: 7px;\n"
"border-radius:15px;\n"
"\n"
"\n"
"}\n"
"QLabel::Hover{\n"
"  top: 0px;\n"
"  left: 0px;\n"
"\n"
"\n"
"}")
        self.applyLabel.setText("")
        self.applyLabel.setObjectName("applyLabel")
        self.applyButton = QtWidgets.QPushButton(missionMenu)
        self.applyButton.setGeometry(QtCore.QRect(10, 90, 111, 41))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        # font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(25)
        self.applyButton.setFont(font)
        self.applyButton.setStyleSheet("QPushButton{\n"
"    color: rgb(255, 255, 255);\n"
" font-size: 18px;\n"
"  font-weight: 200;\n"
"  letter-spacing: 1px;\n"
"  padding-top:5px;\n"
"  outline: 0;\n"
"  border: 3px solid;\n"
"border-radius:15px;\n"
"\n"
"    border-color: rgb(255, 255, 255);\n"
"\n"
"  position: relative;\n"
"  background-color: rgba(0, 255, 0, 0);\n"
"}\n"
"\n"
"QPushButton:Hover{\n"
"position :-5px 5px;\n"
"label.left : -5px;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.502, y2:0.517091, stop:0 rgba(13, 110, 8, 255), stop:1 rgba(36, 225, 42, 255));\n"
"\n"
"\n"
"}")
        self.applyButton.setCheckable(False)
        self.applyButton.setObjectName("applyButton")
        self.stopButton = QtWidgets.QPushButton(missionMenu)
        self.stopButton.setGeometry(QtCore.QRect(10, 150, 101, 41))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        # font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(25)
        self.stopButton.setFont(font)
        self.stopButton.setStyleSheet("QPushButton{\n"
"    color: rgb(255, 255, 255);\n"
" font-size: 18px;\n"
"  font-weight: 200;\n"
"  letter-spacing: 1px;\n"
"padding-top:5px;\n"
"  \n"
"  outline: 0;\n"
"  border: 3px solid;\n"
"border-radius:15px;\n"
"\n"
"    border-color: rgb(255, 255, 255);\n"
"\n"
"  position: relative;\n"
"  background-color: rgba(0, 255, 0, 0);\n"
"}\n"
"\n"
"QPushButton:Hover{\n"
"position :-5px 5px;\n"
"label.left : -5px;\n"
"}\n"
"QPushButton:pressed{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.502, y2:0.517091, stop:0 rgba(13, 110, 8, 255), stop:1 rgba(36, 225, 42, 255));\n"
"\n"
"\n"
"}")
        self.stopButton.setCheckable(False)
        self.stopButton.setObjectName("stopButton")
        self.stopLabel = QtWidgets.QLabel(missionMenu)
        self.stopLabel.setGeometry(QtCore.QRect(10, 160, 101, 41))
        self.stopLabel.setStyleSheet("QLabel{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.502, y2:0.517091, stop:0 rgba(36, 225, 42, 255), stop:1 rgba(13, 110, 8, 255));\n"
"  width: 100%;\n"
"  z-index: -1;\n"
"  position: relative;\n"
"  height: 100%;\n"
"  top: 7px;\n"
"  left: 7px;\n"
"border-radius:15px;\n"
"\n"
"\n"
"}\n"
"QLabel::Hover{\n"
"  top: 0px;\n"
"  left: 0px;\n"
"\n"
"\n"
"}")
        self.stopLabel.setText("")
        self.stopLabel.setObjectName("stopLabel")
        self.label = QtWidgets.QLabel(missionMenu)
        self.label.setGeometry(QtCore.QRect(0, 0, 450, 370))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/logo/Static Images/undersea.jpg"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label.raise_()
        self.stopLabel.raise_()
        self.stopButton.raise_()
        self.comboBox.raise_()
        self.applyLabel.raise_()
        self.applyButton.raise_()

        self.retranslateUi(missionMenu)
        QtCore.QMetaObject.connectSlotsByName(missionMenu)

    def retranslateUi(self, missionMenu):
        _translate = QtCore.QCoreApplication.translate
        missionMenu.setWindowTitle(_translate("missionMenu", "Form"))
        self.comboBox.setItemText(0, _translate("missionMenu", "Mission-1"))
        self.comboBox.setItemText(1, _translate("missionMenu", "Mission-2"))
        self.comboBox.setItemText(2, _translate("missionMenu", "Mission-3"))
        self.comboBox.setItemText(3, _translate("missionMenu", "Mission-4"))
        self.comboBox.setItemText(4, _translate("missionMenu", "Mission-5"))
        self.applyButton.setText(_translate("missionMenu", "APPLY"))
        self.stopButton.setText(_translate("missionMenu", "STOP"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    missionMenu = QtWidgets.QWidget()
    ui = Ui_missionMenu()
    ui.setupUi(missionMenu)
    missionMenu.show()
    sys.exit(app.exec_())


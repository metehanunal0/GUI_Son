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
        missionMenu.setStyleSheet("#missionMenu{\n"
"border-image: url(D:/GUI Son/HighLevel-MMD-Station/Static Images/undersea.jpg);\n"
"}")
        self.comboBox = QtWidgets.QComboBox(missionMenu)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 231, 51))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.comboBox.setFont(font)
        self.comboBox.setStyleSheet("background-color:qlineargradient(spread:pad, x1:0, y1:0.0284091, x2:0.836, y2:0.0336818, stop:0 rgba(0, 198, 0, 255), stop:1 rgba(0, 0, 0, 255));\n"
"\n"
"color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 250, 99);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.applyButton = QtWidgets.QPushButton(missionMenu)
        self.applyButton.setGeometry(QtCore.QRect(10, 90, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        self.applyButton.setFont(font)
        self.applyButton.setStyleSheet("QPushButton{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 1), stop:1 rgba(15, 90, 30, 1));\n"
"color: rgb(255,255,255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 90, 30, 1), stop:1 rgba(0, 0, 0, 1));\n"
"}")
        self.applyButton.setCheckable(False)
        self.applyButton.setObjectName("applyButton")
        self.stopButton_mission = QtWidgets.QPushButton(missionMenu)
        self.stopButton_mission.setGeometry(QtCore.QRect(10, 150, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Montserrat ExtraBold")
        self.stopButton_mission.setFont(font)
        self.stopButton_mission.setStyleSheet("QPushButton{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 1), stop:1 rgba(15, 90, 30, 1));\n"
"color: rgb(255,255,255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 90, 30, 1), stop:1 rgba(0, 0, 0, 1));\n"
"}")
        self.stopButton_mission.setCheckable(False)
        self.stopButton_mission.setObjectName("stopButton_mission")
        self.label = QtWidgets.QLabel(missionMenu)
        self.label.setGeometry(QtCore.QRect(0, 0, 450, 371))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(450, 400))
        self.label.setStyleSheet("\n"
"border-image: url(:/icons/undersea.jpg);\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.raise_()
        self.comboBox.raise_()
        self.applyButton.raise_()
        self.stopButton_mission.raise_()

        self.retranslateUi(missionMenu)
        QtCore.QMetaObject.connectSlotsByName(missionMenu)

    def retranslateUi(self, missionMenu):
        _translate = QtCore.QCoreApplication.translate
        missionMenu.setWindowTitle(_translate("missionMenu", "Mission Menu Window"))
        self.comboBox.setItemText(0, _translate("missionMenu", "Mission-1"))
        self.comboBox.setItemText(1, _translate("missionMenu", "Mission-2"))
        self.comboBox.setItemText(2, _translate("missionMenu", "Mission-3"))
        self.comboBox.setItemText(3, _translate("missionMenu", "Mission-4"))
        self.comboBox.setItemText(4, _translate("missionMenu", "Mission-5"))
        self.applyButton.setText(_translate("missionMenu", "Apply"))
        self.stopButton_mission.setText(_translate("missionMenu", "Stop"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    missionMenu = QtWidgets.QWidget()
    ui = Ui_missionMenu()
    ui.setupUi(missionMenu)
    missionMenu.show()
    sys.exit(app.exec_())


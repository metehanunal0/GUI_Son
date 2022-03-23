# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'casmarinedeneme1.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1840, 1064)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        #palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        #palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        gradient = QtGui.QLinearGradient(0.0751493, 0.068, 0.77605, 0.58)
        gradient.setSpread(QtGui.QGradient.PadSpread)
        gradient.setCoordinateMode(QtGui.QGradient.ObjectBoundingMode)
        gradient.setColorAt(0.0, QtGui.QColor(255, 255, 255))
        gradient.setColorAt(1.0, QtGui.QColor(68, 122, 224))
        brush = QtGui.QBrush(gradient)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        #palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        MainWindow.setStyleSheet("#MainWindow{\n"
"    background-color: qlineargradient(spread:pad, x1:0.0751493, y1:0.068, x2:0.77605, y2:0.58, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(68, 122, 224, 255));\n"
"}")
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.camOne = QtWidgets.QLabel(self.centralwidget)
        self.camOne.setGeometry(QtCore.QRect(10, 40, 720, 540))
        self.camOne.setText("")
        self.camOne.setPixmap(QtGui.QPixmap("../Static Images/on.png"))
        self.camOne.setScaledContents(True)
        self.camOne.setAlignment(QtCore.Qt.AlignCenter)
        self.camOne.setIndent(0)
        self.camOne.setObjectName("camOne")
        self.camTwo = QtWidgets.QLabel(self.centralwidget)
        self.camTwo.setGeometry(QtCore.QRect(740, 40, 720, 540))
        self.camTwo.setText("")
        self.camTwo.setPixmap(QtGui.QPixmap("../Static Images/alt.png"))
        self.camTwo.setScaledContents(True)
        self.camTwo.setAlignment(QtCore.Qt.AlignCenter)
        self.camTwo.setObjectName("camTwo")
        self.autoLight = QtWidgets.QLabel(self.centralwidget)
        self.autoLight.setGeometry(QtCore.QRect(10, 10, 3000, 40))
        self.autoLight.setText("")
        self.autoLight.setPixmap(QtGui.QPixmap("../Static Images/autoOn.png"))
        self.autoLight.setScaledContents(True)
        self.autoLight.setObjectName("autoLight")
        self.pidMenu = QtWidgets.QPushButton(self.centralwidget)
        self.pidMenu.setGeometry(QtCore.QRect(740, 630, 510, 135))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(25)
        self.pidMenu.setFont(font)
        self.pidMenu.setStyleSheet("QPushButton{\n"
" font-size: 40px;\n"
"  font-weight: 200;\n"
"  letter-spacing: 1px;\n"
"  padding: 13px 50px 13px;\n"
"  outline: 0;\n"
"  border: 1px solid;\n"
"border-radius:15px;\n"
"\n"
"  position: relative;\n"
"  background-color: rgba(0, 255, 0, 0);\n"
"}\n"
"\n"
"QPushButton:Hover{\n"
"position :-5px 5px;\n"
"label.left : -5px;\n"
"}\n"
"")
        self.pidMenu.setIconSize(QtCore.QSize(100, 100))
        self.pidMenu.setObjectName("pidMenu")
        self.clockWidget = QtWidgets.QWidget(self.centralwidget)
        self.clockWidget.setGeometry(QtCore.QRect(1470, 185, 360, 271))
        self.clockWidget.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.clockWidget.setObjectName("clockWidget")
        self.stopwatchLcd = QtWidgets.QLCDNumber(self.clockWidget)
        self.stopwatchLcd.setGeometry(QtCore.QRect(0, 0, 361, 141))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setKerning(False)
        self.stopwatchLcd.setFont(font)
        self.stopwatchLcd.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10px;")
        self.stopwatchLcd.setFrameShape(QtWidgets.QFrame.Box)
        self.stopwatchLcd.setLineWidth(3)
        self.stopwatchLcd.setMidLineWidth(1)
        self.stopwatchLcd.setSmallDecimalPoint(False)
        self.stopwatchLcd.setDigitCount(8)
        self.stopwatchLcd.setMode(QtWidgets.QLCDNumber.Dec)
        self.stopwatchLcd.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.stopwatchLcd.setProperty("value", 23146.0)
        self.stopwatchLcd.setProperty("intValue", 23146)
        self.stopwatchLcd.setObjectName("stopwatchLcd")
        self.stopwatchStart = QtWidgets.QPushButton(self.clockWidget)
        self.stopwatchStart.setGeometry(QtCore.QRect(0, 150, 120, 81))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        self.stopwatchStart.setFont(font)
        self.stopwatchStart.setStyleSheet("QPushButton{\n"
" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);\n"
"font-size: 30px;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(85, 170, 0,180);\n"
"}")
        self.stopwatchStart.setObjectName("stopwatchStart")
        self.stopwatchPause = QtWidgets.QPushButton(self.clockWidget)
        self.stopwatchPause.setGeometry(QtCore.QRect(120, 150, 120, 80))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        self.stopwatchPause.setFont(font)
        self.stopwatchPause.setStyleSheet("QPushButton{\n"
" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);\n"
"font-size: 30px;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(85, 170, 0,180);\n"
"}")
        self.stopwatchPause.setObjectName("stopwatchPause")
        self.stopwatchStop = QtWidgets.QPushButton(self.clockWidget)
        self.stopwatchStop.setGeometry(QtCore.QRect(240, 150, 120, 80))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        self.stopwatchStop.setFont(font)
        self.stopwatchStop.setStyleSheet("QPushButton{\n"
" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);\n"
"font-size: 30px;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"background-color: rgba(85, 170, 0,180);\n"
"}")
        self.stopwatchStop.setObjectName("stopwatchStop")
        self.label_5 = QtWidgets.QLabel(self.clockWidget)
        self.label_5.setGeometry(QtCore.QRect(0, 180, 121, 61))
        self.label_5.setStyleSheet("QLabel{\n"
"    background-color: rgb(187, 158, 217);\n"
"  width: 100%;\n"
"  z-index: -1;\n"
"  position: relative;\n"
"  height: 100%;\n"
"  top: 7px;\n"
"  left: 7px;\n"
"border-radius:10px;\n"
"\n"
"\n"
"}\n"
"QLabel::Hover{\n"
"  top: 0px;\n"
"  left: 0px;\n"
"\n"
"\n"
"}")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.clockWidget)
        self.label_6.setGeometry(QtCore.QRect(120, 180, 121, 61))
        self.label_6.setStyleSheet("QLabel{\n"
"    background-color: rgb(187, 158, 217);\n"
"  width: 100%;\n"
"  z-index: -1;\n"
"  position: relative;\n"
"  height: 100%;\n"
"  top: 7px;\n"
"  left: 7px;\n"
"border-radius:10px;\n"
"\n"
"\n"
"}\n"
"QLabel::Hover{\n"
"  top: 0px;\n"
"  left: 0px;\n"
"\n"
"\n"
"}")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.clockWidget)
        self.label_7.setGeometry(QtCore.QRect(240, 180, 121, 61))
        self.label_7.setStyleSheet("QLabel{\n"
"    background-color: rgb(187, 158, 217);\n"
"  width: 100%;\n"
"  z-index: -1;\n"
"  position: relative;\n"
"  height: 100%;\n"
"  top: 7px;\n"
"  left: 7px;\n"
"border-radius:10px;\n"
"\n"
"\n"
"}\n"
"QLabel::Hover{\n"
"  top: 0px;\n"
"  left: 0px;\n"
"\n"
"\n"
"}")
        self.label_7.setText("")
        self.label_7.setObjectName("label_7")
        self.stopwatchLcd.raise_()
        self.label_7.raise_()
        self.label_6.raise_()
        self.label_5.raise_()
        self.stopwatchStart.raise_()
        self.stopwatchPause.raise_()
        self.stopwatchStop.raise_()
        self.valuesWidget = QtWidgets.QWidget(self.centralwidget)
        self.valuesWidget.setGeometry(QtCore.QRect(1470, 445, 360, 351))
        self.valuesWidget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.valuesWidget.setObjectName("valuesWidget")
        self.pressureLabel = QtWidgets.QLabel(self.valuesWidget)
        self.pressureLabel.setGeometry(QtCore.QRect(10, 19, 161, 51))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(20)
        self.pressureLabel.setFont(font)
        self.pressureLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 255, 255)")
        self.pressureLabel.setObjectName("pressureLabel")
        self.depthLabel = QtWidgets.QLabel(self.valuesWidget)
        self.depthLabel.setGeometry(QtCore.QRect(70, 80, 101, 60))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(20)
        self.depthLabel.setFont(font)
        self.depthLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 255, 255)")
        self.depthLabel.setObjectName("depthLabel")
        self.pressureLcd = QtWidgets.QLCDNumber(self.valuesWidget)
        self.pressureLcd.setGeometry(QtCore.QRect(190, 10, 160, 60))
        self.pressureLcd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pressureLcd.setStyleSheet(" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);")
        self.pressureLcd.setMidLineWidth(0)
        self.pressureLcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.pressureLcd.setProperty("intValue", 0)
        self.pressureLcd.setObjectName("pressureLcd")
        self.depthLcd = QtWidgets.QLCDNumber(self.valuesWidget)
        self.depthLcd.setGeometry(QtCore.QRect(190, 80, 160, 60))
        self.depthLcd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.depthLcd.setStyleSheet(" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);")
        self.depthLcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.depthLcd.setObjectName("depthLcd")
        self.eulerWidget = QtWidgets.QWidget(self.valuesWidget)
        self.eulerWidget.setGeometry(QtCore.QRect(0, 140, 360, 211))
        self.eulerWidget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.eulerWidget.setObjectName("eulerWidget")
        self.headLabel = QtWidgets.QLabel(self.eulerWidget)
        self.headLabel.setGeometry(QtCore.QRect(90, 10, 80, 60))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(20)
        self.headLabel.setFont(font)
        self.headLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 255, 255)")
        self.headLabel.setObjectName("headLabel")
        self.headLcd = QtWidgets.QLCDNumber(self.eulerWidget)
        self.headLcd.setGeometry(QtCore.QRect(190, 10, 160, 60))
        self.headLcd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.headLcd.setStyleSheet(" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);")
        self.headLcd.setMidLineWidth(0)
        self.headLcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.headLcd.setProperty("intValue", 0)
        self.headLcd.setObjectName("headLcd")
        self.pitchLabel = QtWidgets.QLabel(self.eulerWidget)
        self.pitchLabel.setGeometry(QtCore.QRect(80, 80, 121, 60))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(20)
        self.pitchLabel.setFont(font)
        self.pitchLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 255, 255)")
        self.pitchLabel.setObjectName("pitchLabel")
        self.pitchLcd = QtWidgets.QLCDNumber(self.eulerWidget)
        self.pitchLcd.setGeometry(QtCore.QRect(190, 80, 160, 60))
        self.pitchLcd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pitchLcd.setStyleSheet(" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);")
        self.pitchLcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.pitchLcd.setObjectName("pitchLcd")
        self.rollLabel = QtWidgets.QLabel(self.eulerWidget)
        self.rollLabel.setGeometry(QtCore.QRect(100, 150, 81, 60))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(20)
        self.rollLabel.setFont(font)
        self.rollLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0);\n"
"color: rgb(255, 255, 255)")
        self.rollLabel.setObjectName("rollLabel")
        self.rollLcd = QtWidgets.QLCDNumber(self.eulerWidget)
        self.rollLcd.setGeometry(QtCore.QRect(190, 150, 160, 60))
        self.rollLcd.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.rollLcd.setStyleSheet(" background-color: #dcbaff;\n"
"color: rgb(255, 255, 255);")
        self.rollLcd.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rollLcd.setObjectName("rollLcd")
        self.cameraOneCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.cameraOneCheck.setGeometry(QtCore.QRect(10, 590, 181, 21))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        self.cameraOneCheck.setFont(font)
        self.cameraOneCheck.setStyleSheet("color: rgb(0,0,0);\n"
"font-size:30px;")
        self.cameraOneCheck.setObjectName("cameraOneCheck")
        self.cameraTwoCheck = QtWidgets.QCheckBox(self.centralwidget)
        self.cameraTwoCheck.setGeometry(QtCore.QRect(740, 590, 201, 20))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        self.cameraTwoCheck.setFont(font)
        self.cameraTwoCheck.setStyleSheet("color: rgb(0,0,0);\n"
"font-size:30px;")
        self.cameraTwoCheck.setObjectName("cameraTwoCheck")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(1670, 810, 135, 135))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../Static Images/CAS Logo Beyaz.png"))
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.Bayrak = QtWidgets.QLabel(self.centralwidget)
        self.Bayrak.setGeometry(QtCore.QRect(1520, 10, 264, 174))
        self.Bayrak.setText("")
        self.Bayrak.setPixmap(QtGui.QPixmap("../Static Images/bayrak.png"))
        self.Bayrak.setScaledContents(True)
        self.Bayrak.setObjectName("Bayrak")
        self.pushButton_screenshot = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_screenshot.setGeometry(QtCore.QRect(570, 660, 131, 71))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(25)
        self.pushButton_screenshot.setFont(font)
        self.pushButton_screenshot.setStyleSheet("QPushButton{\n"
" font-size: 15px;\n"
"  font-weight: 200;\n"
"  letter-spacing: 1px;\n"
"  \n"
"  outline: 0;\n"
"  border: 1px solid;\n"
"border-radius:15px;\n"
"\n"
"  position: relative;\n"
"  background-color: rgba(0, 255, 0, 0);\n"
"}\n"
"\n"
"QPushButton:Hover{\n"
"position :-5px 5px;\n"
"label.left : -5px;\n"
"}\n"
"")
        self.pushButton_screenshot.setCheckable(False)
        self.pushButton_screenshot.setObjectName("pushButton_screenshot")
        self.missionMenu = QtWidgets.QPushButton(self.centralwidget)
        self.missionMenu.setGeometry(QtCore.QRect(10, 630, 510, 135))
        font = QtGui.QFont()
        font.setFamily("8-bit Operator+ 8")
        font.setPointSize(-1)
        font.setBold(False)
        font.setWeight(25)
        self.missionMenu.setFont(font)
        self.missionMenu.setStyleSheet("QPushButton{\n"
" font-size: 40px;\n"
"  font-weight: 200;\n"
"  letter-spacing: 1px;\n"
"  padding: 13px 50px 13px;\n"
"  outline: 0;\n"
"  border: 1px solid;\n"
"border-radius:15px;\n"
"\n"
"  position: relative;\n"
"  background-color: rgba(0, 255, 0, 0);\n"
"}\n"
"\n"
"QPushButton:Hover{\n"
"position :-5px 5px;\n"
"label.left : -5px;\n"
"}\n"
"")
        self.missionMenu.setIconSize(QtCore.QSize(100, 100))
        self.missionMenu.setObjectName("missionMenu")
        self.ytulogo = QtWidgets.QLabel(self.centralwidget)
        self.ytulogo.setGeometry(QtCore.QRect(1500, 810, 151, 131))
        self.ytulogo.setStyleSheet("border-image: url(D:/GUISon_v2/HighLevel-MMD-Station/background/ytu.png);")
        self.ytulogo.setText("")
        self.ytulogo.setAlignment(QtCore.Qt.AlignCenter)
        self.ytulogo.setObjectName("ytulogo")
        self.caslogo = QtWidgets.QLabel(self.centralwidget)
        self.caslogo.setGeometry(QtCore.QRect(1350, 820, 131, 121))
        self.caslogo.setStyleSheet("border-image:url(D:/GUISon_v2/HighLevel-MMD-Station/background/casmarine_yesil_yuvarlak.png)")
        self.caslogo.setText("")
        self.caslogo.setObjectName("caslogo")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(760, 650, 510, 135))
        self.label_2.setStyleSheet("QLabel{\n"
" background-color: #dcbaff;\n"
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
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 650, 510, 135))
        self.label_3.setStyleSheet("QLabel{\n"
" background-color: #dcbaff;\n"
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
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(580, 670, 131, 71))
        self.label_4.setStyleSheet("QLabel{\n"
" background-color: #dcbaff;\n"
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
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.label_4.raise_()
        self.label_3.raise_()
        self.label_2.raise_()
        self.camOne.raise_()
        self.camTwo.raise_()
        self.autoLight.raise_()
        self.pidMenu.raise_()
        self.clockWidget.raise_()
        self.valuesWidget.raise_()
        self.cameraOneCheck.raise_()
        self.cameraTwoCheck.raise_()
        self.label.raise_()
        self.Bayrak.raise_()
        self.pushButton_screenshot.raise_()
        self.missionMenu.raise_()
        self.ytulogo.raise_()
        self.caslogo.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.actionMission_1 = QtWidgets.QAction(MainWindow)
        self.actionMission_1.setObjectName("actionMission_1")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CASMARINE VIII Graphical User Interface"))
        self.pidMenu.setText(_translate("MainWindow", "PID Menu"))
        self.stopwatchStart.setText(_translate("MainWindow", "Start"))
        self.stopwatchPause.setText(_translate("MainWindow", "Pause"))
        self.stopwatchStop.setText(_translate("MainWindow", "Stop"))
        self.pressureLabel.setText(_translate("MainWindow", "Pressure :"))
        self.depthLabel.setText(_translate("MainWindow", "Depth :"))
        self.headLabel.setText(_translate("MainWindow", "Head :"))
        self.pitchLabel.setText(_translate("MainWindow", "Pitch :"))
        self.rollLabel.setText(_translate("MainWindow", "Roll :"))
        self.cameraOneCheck.setText(_translate("MainWindow", "Front Cam"))
        self.cameraTwoCheck.setText(_translate("MainWindow", "Bottom Cam"))
        self.pushButton_screenshot.setText(_translate("MainWindow", "Screenshot"))
        self.missionMenu.setText(_translate("MainWindow", "Mission Menu"))
        self.actionMission_1.setText(_translate("MainWindow", "Mission-1"))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


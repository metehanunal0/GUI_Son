from pidMenuFace import Ui_pidMenu
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *
import json

from PyQt5 import QtCore, QtGui, QtWidgets

class PidMenuBack(QTabWidget):
    def __init__(self, qPid):
        super().__init__()
        self.ui= Ui_pidMenu()
        self.qPid = qPid  # Communication line : 339
        self.ui.setupUi(self)
        self.jsonData = None
        self.jsonPid = None
        self.ui.PIDApply.clicked.connect(self.applyFunction)

        self.pidcValues = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.pidcTags = ["Roll P", "Roll I", "Roll D",
                         "Depth P", "Depth I", "Depth D",
                         "Pitch P", "Pitch I", "Pitch D",
                         ]
        self.pidcObjects = [self.roll_P, self.roll_I, self.roll_D,
                            self.depth_P, self.depth_I, self.depth_D,
                            self.pitch_P, self.pitch_I, self.pitch_D
                            ]

    def printToScreen(self):
        for i in range(9):
            self.pidcObjects[i].setText(f"{self.pidcValues[i]}")

    def getFromScreen(self):
        for i in range(9):
            self.pidcValues[i] = int(self.pidcObjects[i].text())

    def applyFunction(self):
        self.getFromScreen()
        self.transmitDatav2()

    def transmitDatav2(self):
        data = self.pidcValues
        print(data)
        data = bytearray(data)
        try:
            self.qPid.put(data, timeout=0.00001)
        except:
            pass

    def show(self):
        QtWidgets.QTabWidget.show(self)
        self.jsonLoader()
        self.printToScreen()
        # self.transmitDatav2()

    def jsonLoader(self):
        f = open("dataBase.json", "r")
        self.jsonData = json.load(f)
        self.jsonPid = self.jsonData["pidMenu"]
        f.close()
        for i in range(9):
            self.pidcValues[i] = self.jsonPid[self.pidcTags[i]]

    def jsonDumper(self):  # Dump all of the data to the json database
        # self.jsonLoader()  # This is for checking if other data (thruster, button conf) changed
        self.getFromScreen()
        zipper = zip(self.pidcTags, self.pidcValues)
        jsonSave = dict(zipper)
        jsonSave = {"pidMenu": jsonSave}
        self.jsonData.update(jsonSave)
        f = open("dataBase.json", "w")
        json.dump(self.jsonData, f, separators=(" , ", ":"), indent=4)
        f.close()

    def closeEvent(self, event):
        box = QtWidgets.QMessageBox()
        box.setIcon(QtWidgets.QMessageBox.Question)
        box.setWindowTitle('Çıkış')
        box.setText('Çıkış yaparken verilerin kaydedilmesini ister misiniz?')
        box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Abort)
        buttonY = box.button(QtWidgets.QMessageBox.Yes)
        buttonY.setText('Kaydet ve Çık')
        buttonN = box.button(QtWidgets.QMessageBox.No)
        buttonN.setText('Çıkış Yapma')
        buttonZ = box.button(QtWidgets.QMessageBox.Abort)
        buttonZ.setText('Kaydetmeden Çık')
        box.exec_()
        if box.clickedButton() == buttonZ:
            self.jsonData = None
            self.jsonPid = None
            self.timer.stop()
            event.accept()
        elif box.clickedButton() == buttonY:
            self.jsonDumper()
            self.jsonData = None
            self.jsonPid = None
            self.timer.stop()
            event.accept()
        else:
            event.ignore()

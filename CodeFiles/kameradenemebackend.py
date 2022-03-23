import multiprocessing
import threading

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QRunnable, QThreadPool, QObject
import queue
from multiprocessing import Process, Queue
import numpy as np
import casmarine8_10_1, pidMenu, collections, datetime, cv2, json, socket, struct
import time
import photomosaic_main
from missionMenu import *


# import mission2cam
# Thrust, Task, PID, haberleşmeye,
# Button, Uplink arayüze gönderilecek.
class signalClass(QObject):
    change_pixmap_signal = pyqtSignal(np.ndarray)


class VideoThread(QRunnable):
    def __init__(self, camName: str, qFrontCam : Queue, qBottomCam: Queue):
        super().__init__()
        self.camName = str
        self.signals = signalClass()
        self._run_flag = True
        self._pause_flag = True,
        if camName == "frontCam":
            self.q = qFrontCam
        elif camName == "bottomCam":
            self.q = qBottomCam
        else:
            self.q = None
    def main_loop(self):
        #dump buffer
        self.img = self.q.get()
        self.signals.change_pixmap_signal.emit(self.img)
    def run(self):
        while self._run_flag:
            self.main_loop()
            if self._pause_flag:
                self.signals.change_pixmap_signal.emit(self.camJpg)
            time.sleep(0.5)
def stop(self):
    """Sets run flag to False and waits for thread to finish"""
    self._pause_flag = True
    self._run_flag = False
    # self.wait()

# noinspection PyUnresolvedReferences
class CASMarine8(QtWidgets.QMainWindow, casmarine8_10_1.Ui_MainWindow):
    def __init__(self, qUplink, qPid, qTask):
        QtWidgets.QMainWindow.__init__(self)
        self.now = None
        self.string = None
        self.setupUi(self)
        self.clKiller = collections.deque(maxlen=1)
        # self.pidwin = PidMenuBack(qPid)  # qPid Values are sent in Pid menu backend class (line : 273, 348)
        # self.pidwin.jsonLoader()
        # self.pidwin.transmitData()

        self.activeButtonIndex = list()  # This is for starting an example list
        self.transmitData = [1, 0, 1, 0, 1, 0, 1, 0]  # This is for starting an example list #kapayınca hata veriyo mq
        self.stopwatchLcd.display("0:0.00")
        self.qUplink = qUplink
        self.qTask = qTask
        self.setWindowIcon(QtGui.QIcon("../Static Images/CASLogo.png"))
        self.timer = QTimer()  # This timer is for stopwatch
        self.timer.timeout.connect(self.stopwatch)
        self.counter = 0
        self.timeLast = 0
        self.timeNow = 0
        self.stopwatchStart.clicked.connect(self.startStopwatch)
        self.stopwatchPause.clicked.connect(self.pauseStopwatch)
        self.stopwatchStop.clicked.connect(self.stopStopwatch)

        self.threadPool = QThreadPool.globalInstance()
        self.thread = VideoThread(camName="frontCam")
        self.thread.signals.change_pixmap_signal.connect(self.update_image)

        self.cameraOneCheck.stateChanged.connect(self.cameraOneState)
        self.threadPool.start(self.thread)

        self.thread2 = VideoThread(camName="bottomCam")
        self.thread2.signals.change_pixmap_signal.connect(self.update_imageTwo)
        self.cameraTwoCheck.stateChanged.connect(self.cameraTwoState)
        self.threadPool.start(self.thread2)


        self.pidMenu.clicked.connect(self.pidWindow)
        self.pushButton_screenshot.clicked.connect(self.screenShot)
        self.mission_object = InitializeMissionMenu()
        self.missionMenu.clicked.connect(self.missionWindow)
        self.mission_object.mission_signal.connect(self.selectMission)

        self.mission = None



        # This holds comm values in a dictionary for ease of use, bottom has tags required for zip
        self.receivedDataDict = {"Pressure": 15, "Temperature": 20, "Depth": 2,
                                 "Head": 110, "Pitch": 14, "Roll": 5, "Auto": False}
        self.receivedDataTags = ["Pressure", "Temperature", "Depth", "Head", "Pitch", "Roll", "Auto"]

        # self.rot = ImageSource.Rotator()  # This is for visualizing angle values this class has required functions

        # These codes hold memory value for fast changing of autonomous light value
        self.autoLightOff = cv2.imread("../Static Images/autoOff.png")
        self.autoLightOff = self.convert_cv_qt(self.autoLightOff, horizontal=1450, vertical=20)
        self.autoLightOn = cv2.imread("../Static Images/autoOn.png")
        self.autoLightOn = self.convert_cv_qt(self.autoLightOn, horizontal=1450, vertical=20)

        self.dataSignalDelay = QTimer()  # This timer is for communication delay
        self.dataSignalDelay.timeout.connect(self.communicate)  # Communicate function line : 204
        self.dataSignalDelay.start(20)  # This is communication function transmission speed

        self.lcd_list = list()

    @pyqtSlot(int)
    def selectMission(self, mission): #değişcek
        mission = bytearray(mission)
        self.qTask.put(mission)


    def missionWindow(self):
        self.mission_object.show()

    def closeEvent(self, event):
        self.thread.stop()
        self.thread2.stop()
        self.threadPool.waitForDone(1000)
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, image):
        """Updates the image_label with a new opencv image"""
        qtImage = self.convert_cv_qt(image, 720, 540)
        self.camOne.setPixmap(qtImage)

    def cameraOneState(self):
        if self.cameraOneCheck.isChecked():
            self.thread._pause_flag = False
        elif not self.cameraOneCheck.isChecked():
            self.thread._pause_flag = True

    @pyqtSlot(np.ndarray)
    def update_imageTwo(self, image):
        """Updates the image_label with a new opencv image"""
        qtImage = self.convert_cv_qt(image, 720, 540)
        self.camTwo.setPixmap(qtImage)

    def cameraTwoState(self):
        if self.cameraTwoCheck.isChecked():
            self.thread2._pause_flag = False
        elif not self.cameraTwoCheck.isChecked():
            self.thread2._pause_flag = True

    def convert_cv_qt(self, cv_img, horizontal=720, vertical=405):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(horizontal, vertical, Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)

    def pidWindow(self):
        self.pidwin.show()

    def screenShot(self, qFrameIn : Queue): #HATA
        #haberleşme lazım qFrameIn
        photomosaic_main.wreck(qFrameIn) #hata

    def stopwatch(self):
        self.now = datetime.datetime.now()
        self.timeNow = self.now.second + self.now.minute * 60 + self.now.microsecond * 0.000001
        self.counter += self.timeNow - self.timeLast
        self.timeLast = self.timeNow
        self.updateStopwatchLcd(self.counter)

    def startStopwatch(self):
        self.now = datetime.datetime.now()
        self.timeLast = self.now.minute * 60 + self.now.second + self.now.microsecond * 0.000001
        self.timeNow = self.now.minute * 60 + self.now.second + self.now.microsecond * 0.000001
        self.timer.start(100)

    def pauseStopwatch(self):
        self.timer.stop()

    def stopStopwatch(self):
        self.timer.stop()
        self.counter = 0
        self.updateStopwatchLcd(0)

    def updateStopwatchLcd(self, secondData):
        self.string = f"{int(secondData / 60)}:{secondData % 60:.2f}"
        self.stopwatchLcd.display(self.string)

    def communicate(self):
        try:  # Uplink que get command
            upLinkData = self.qUplink.get(timeout=0.00001)
            self.receivedDataDict["Roll"] = struct.unpack('h', upLinkData[0:2])[0]  # Struct send data in a tupple
            self.receivedDataDict["Pitch"] = struct.unpack('h', upLinkData[2:4])[0]  # we get only 1 data
            self.receivedDataDict["Head"] = struct.unpack('h', upLinkData[4:6])[0]
            self.receivedDataDict["Temperature"] = struct.unpack('f', upLinkData[6:10])[0]
            self.receivedDataDict["Pressure"] = struct.unpack('h', upLinkData[10:12])[0]
            self.receivedDataDict["Depth"] = struct.unpack('f', upLinkData[12:16])[0]

            # Zip upLinkData with self.receivedDataTags to create dict and merge with self.receivedDataDict
            self.autoState(self.receivedDataDict["Auto"])

            self.lcdUpdater()
            #self.angleImageUpdater(self.receivedDataDict["Roll"], -1 * self.receivedDataDict["Pitch"])             # BU NEDİR? NE İŞE YARAMAKTADIR?
        except queue.Empty:
            pass

    def lcdUpdater(self):
        self.pressureLcd.display(self.receivedDataDict["Pressure"])
        self.depthLcd.display(self.receivedDataDict["Depth"])
        self.headLcd.display(self.receivedDataDict["Head"])
        self.pitchLcd.display(self.receivedDataDict["Pitch"])
        self.rollLcd.display(self.receivedDataDict["Roll"])

    def autoState(self, state=False):
        if state:
            self.autoLight.setPixmap(self.autoLightOn)
        elif not state:
            self.autoLight.setPixmap(self.autoLightOff)


# noinspection PyUnresolvedReferences,PyTypeChecker
# class PidMenuBack(QtWidgets.QTabWidget, pidMenu.Ui_pidMenu):
#     def __init__(self, qPid):
#         QtWidgets.QTabWidget.__init__(self)
#         self.qPid = qPid  # Communication line : 339
#         self.setupUi(self)
#         self.setFixedSize(550, 700)
#         self.currentChanged.connect(self.tabChange)
#         self.jsonData = None
#         self.jsonPid = None
#         self.PIDApply.clicked.connect(self.applyFunction)
#         self.servoApply.clicked.connect(self.applyFunction)
#         self.pidcValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 0, 0, 0]
#         self.pidcTags = ["Roll P", "Roll I", "Roll D",
#                          "Depth P", "Depth I", "Depth D",
#                          "Pitch P", "Pitch I", "Pitch D"]
#         self.pidcObjects = [self.roll_P, self.roll_I, self.roll_D,
#                             self.depth_P, self.depth_I, self.depth_D,
#                             self.pitch_P, self.pitch_I, self.pitch_D]
#
#         for i in range(len(self.pidcObjects)):
#             self.pidcObjects[i].setValidator(QtGui.QIntValidator(0, 255))
#
#         self.timer = QTimer()
#         self.timer.timeout.connect(self.dataExchange)
#
#
#     def tabChange(self):
#         if self.currentIndex() == 0:
#             self.setFixedSize(550, 700)
#         elif self.currentIndex() == 1:
#             self.setFixedSize(420, 330)
#
#     def printToScreen(self):
#         for i in range(9):
#             self.pidcObjects[i].setText(f"{self.pidcValues[i]}")
#
#
#     def getFromScreen(self):
#         for i in range(9):
#             self.pidcValues[i] = int(self.pidcObjects[i].text())
#
#
#     def applyFunction(self):
#         self.getFromScreen()
#         self.transmitData()
#
#     def transmitData(self):
#         data = self.pidcValues[0:9]
#         data[4:8], data[8:12], data[12:16] = data[12:16], data[4:8], data[8:12]
#         data[1], data[2], data[5], data[6], data[9], data[10], data[13], data[14] = data[2], data[1], data[6], data[5], \
#                                                                                     data[10], data[9], data[14], data[
#                                                                                         13]
#         data[16:23] = data[21], data[22], data[19], data[20], data[16], data[17], data[18]
#         data = bytearray(data)
#         try:
#             self.qPid.put(data, timeout=0.00001)
#
#         except:
#             pass
#
#     def dataExchange(self):
#         if self.slider1Check.isChecked():
#             choice = self.slider1Choice.currentText()
#             if self.sliderTags.index(choice) > 0:
#                 choiceIndex = self.pidcTags.index(choice)
#                 if self.lastChoiceIndex[0] is not None and self.lastChoiceIndex[0] != choiceIndex:
#                     self.pidcObjects[self.lastChoiceIndex[0]].setReadOnly(False)
#                 self.lastChoiceIndex[0] = choiceIndex
#                 self.pidcObjects[choiceIndex].setReadOnly(True)
#                 self.pidcObjects[choiceIndex].setText(str(self.slider1.value()))
#         else:
#             if self.lastChoiceIndex[0] is not None:
#                 self.pidcObjects[self.lastChoiceIndex[0]].setReadOnly(False)
#
#         if self.slider2Check.isChecked():
#             choice = self.slider2Choice.currentText()
#             if self.sliderTags.index(choice) > 0:
#                 choiceIndex = self.pidcTags.index(choice)
#                 if self.lastChoiceIndex[1] is not None and self.lastChoiceIndex[1] != choiceIndex:
#                     self.pidcObjects[self.lastChoiceIndex[1]].setReadOnly(False)
#                 self.lastChoiceIndex[1] = choiceIndex
#                 self.pidcObjects[choiceIndex].setReadOnly(True)
#                 self.pidcObjects[choiceIndex].setText(str(self.slider2.value()))
#         else:
#             if self.lastChoiceIndex[1] is not None:
#                 self.pidcObjects[self.lastChoiceIndex[1]].setReadOnly(False)
#
#         if self.slider3Check.isChecked():
#             choice = self.slider3Choice.currentText()
#             if self.sliderTags.index(choice) > 0:
#                 choiceIndex = self.pidcTags.index(choice)
#                 if self.lastChoiceIndex[2] is not None and self.lastChoiceIndex[2] != choiceIndex:
#                     self.pidcObjects[self.lastChoiceIndex[2]].setReadOnly(False)
#                 self.lastChoiceIndex[2] = choiceIndex
#                 self.pidcObjects[choiceIndex].setReadOnly(True)
#                 self.pidcObjects[choiceIndex].setText(str(self.slider3.value()))
#         else:
#             if self.lastChoiceIndex[2] is not None:
#                 self.pidcObjects[self.lastChoiceIndex[2]].setReadOnly(False)
#
#         self.transmitData()
#
#     def timerConfig(self):
#         if self.slider1Check.isChecked() or self.slider2Check.isChecked() or self.slider3Check.isChecked():
#             if not self.timer.isActive():
#                 self.timer.start(2)
#         else:
#             for i in self.lastChoiceIndex:
#                 if i is not None:
#                     self.pidcObjects[i].setReadOnly(False)
#             self.timer.stop()
#
#     def show(self):
#         QtWidgets.QTabWidget.show(self)
#         self.jsonLoader()
#         self.printToScreen()
#         self.transmitData()
#
#     def jsonLoader(self):
#         f = open("dataBase.json", "r")
#         self.jsonData = json.load(f)
#         self.jsonPid = self.jsonData["pidMenu"]
#         f.close()
#         for i in range(9):
#             self.pidcValues[i] = self.jsonPid[self.pidcTags[i]]
#
#     def jsonDumper(self):  # Dump all of the data to the json database
#         self.jsonLoader()  # This is for checking if other data (thruster, button conf) changed
#         self.getFromScreen()
#         zipper = zip(self.pidcTags, self.pidcValues)
#         jsonSave = dict(zipper)
#         jsonSave = {"pidMenu": jsonSave}
#         self.jsonData.update(jsonSave)
#         f = open("dataBase.json", "w")
#         json.dump(self.jsonData, f, separators=(" , ", ":"), indent=4)
#         f.close()
#
#     def closeEvent(self, event):
#         box = QtWidgets.QMessageBox()
#         box.setIcon(QtWidgets.QMessageBox.Question)
#         box.setWindowTitle('Çıkış')
#         box.setText('Çıkış yaparken verilerin kaydedilmesini ister misiniz?')
#         box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Abort)
#         buttonY = box.button(QtWidgets.QMessageBox.Yes)
#         buttonY.setText('Kaydet ve Çık')
#         buttonN = box.button(QtWidgets.QMessageBox.No)
#         buttonN.setText('Çıkış Yapma')
#         buttonZ = box.button(QtWidgets.QMessageBox.Abort)
#         buttonZ.setText('Kaydetmeden Çık')
#         box.exec_()
#         if box.clickedButton() == buttonZ:
#             self.jsonData = None
#             self.jsonPid = None
#             self.timer.stop()
#             event.accept()
#         elif box.clickedButton() == buttonY:
#             self.jsonDumper()
#             self.jsonData = None
#             self.jsonPid = None
#             self.timer.stop()
#             event.accept()
#         else:
#             event.ignore()




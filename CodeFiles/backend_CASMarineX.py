from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QRunnable, QThreadPool, QObject
from multiprocessing import Queue
import numpy as np
import collections, datetime, cv2, json, struct
import mainMenuFace
import pidMenu
import photomosaic_main
from missionMenu import *

# -------------------  define signal for camera update  -------------
class signalClass(QObject):
    change_pixmap_signal = pyqtSignal(np.ndarray)

# ------------ optimized thread class for video stream update ------------
class VideoThread(QRunnable):
    def __init__(self, qCam: Queue):
        super().__init__()
        self.signals = signalClass()
        self._run_flag = True
        self._pause_flag = True
        self.img = None
        self.camJpg = cv2.imread("../Static Images/cam_icon.jpeg")
        self.q = qCam

    def run(self):
        while True:
            try:
                self.img = self.q.get()
                self.signals.change_pixmap_signal.emit(self.img)
            except:
                print("cant get image")

            if self._pause_flag:
                self.signals.change_pixmap_signal.emit(self.camJpg)
            # time.sleep(0.5)


    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._pause_flag = True
        self._run_flag = False
        # self.wait()

""" CASMarineX is general function that leads us to perform Queue activity and make the communication alright"""
# noinspection PyUnresolvedReferences
class CASMarineX(QtWidgets.QMainWindow, mainMenuFace.Ui_MainWindow):
    def __init__(self, qUplink, qPid, qTask, qFrontCam, qBottomCam):
        QtWidgets.QMainWindow.__init__(self)
        self.now = None
        self.string = None
        self.setupUi(self)
        self.clKiller = collections.deque(maxlen=1)

        self.pidwin = PidMenuBack(qPid)  # qPid Values are sent in Pid menu backend class
        self.pidwin.jsonLoader()
        self.pidwin.transmitDatav2()

        self.qFrontCam = qFrontCam
        self.qBottomCam = qBottomCam
        self.qUplink = qUplink
        self.qTask = qTask

        # self.activeButtonIndex = list()  # This is for starting an example list
        self.transmitData = [1, 0, 1, 0, 1, 0, 1, 0]  # This is for starting an example list
        self.stopwatchLcd.display("0:0.00")

        self.setWindowIcon(QtGui.QIcon("../Static Images/CASLogo.png"))

        # ------ stopwatch are being built -----
        self.timer = QTimer()
        self.timer.timeout.connect(self.stopwatch)
        self.counter = 0
        self.timeLast = 0
        self.timeNow = 0
        self.stopwatchStart.clicked.connect(self.startStopwatch)
        self.stopwatchPause.clicked.connect(self.pauseStopwatch)
        self.stopwatchStop.clicked.connect(self.stopStopwatch)

        # -------- performs two video stream activity simultaneously -------
        self.threadPool = QThreadPool().globalInstance()
        self.thread = VideoThread(qCam=qFrontCam)
        self.thread.signals.change_pixmap_signal.connect(self.updateFrontCam)
        self.cameraOneCheck.stateChanged.connect(self.cameraOneState)
        self.threadPool.start(self.thread)
        self.thread2 = VideoThread(qCam=qBottomCam)
        self.thread2.signals.change_pixmap_signal.connect(self.updateBottomCam)
        self.cameraTwoCheck.stateChanged.connect(self.cameraTwoState)
        self.threadPool.start(self.thread2)


        self.pidMenu.clicked.connect(self.pidWindow)
        self.screenshotButton.clicked.connect(self.screenShot)
        self.mission_object = InitializeMissionMenu()
        self.missionMenu.clicked.connect(self.missionWindow)
        self.mission_object.mission_signal.connect(self.selectMission)

        # This holds comm values in a dictionary for ease of use, bottom has tags required for zip
        self.receivedDataDict = {"Pressure": 15, "Depth": 2,
                                 "Head": 110, "Pitch": 14, "Roll": 5, "Auto": False}
        self.receivedDataTags = ["Pressure", "Depth", "Head", "Pitch", "Roll", "Auto"]

        # These codes hold memory value for fast changing of autonomous light value
        self.autoLightOff = cv2.imread("../Static Images/autoOff.png")
        self.autoLightOff = self.convert_cv_qt(self.autoLightOff, horizontal=1450, vertical=20)
        self.autoLightOn = cv2.imread("../Static Images/autoOn.png")
        self.autoLightOn = self.convert_cv_qt(self.autoLightOn, horizontal=1450, vertical=20)

        self.dataSignalDelay = QTimer()  # This timer is for communication delay
        self.dataSignalDelay.timeout.connect(self.communicate)  # Communicate function line : 198
        self.dataSignalDelay.start(20)  # This is communication function transmission speed

        self.lcd_list = list()

    @pyqtSlot(int)
    def selectMission(self, mission):
        self.qTask.put(bytearray(mission))

    def missionWindow(self):
        self.mission_object.show()

    def closeEvent(self, event):
        self.thread.stop()
        self.thread2.stop()
        self.threadPool.waitForDone(1000)
        event.accept()

    @pyqtSlot(np.ndarray)
    def updateFrontCam(self, image):
        """Updates the image_label with a new opencv image"""
        qtImage = self.convert_cv_qt(image, 720, 540)
        self.camOne.setPixmap(qtImage)

    def cameraOneState(self):
        if self.cameraOneCheck.isChecked():
            self.thread._pause_flag = False
        elif not self.cameraOneCheck.isChecked():
            self.thread._pause_flag = True

    @pyqtSlot(np.ndarray)
    def updateBottomCam(self, image):
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

    def screenShot(self):
        photomosaic_main.wreck(self.qBottomCam)

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
            self.receivedDataDict["Pressure"] = struct.unpack('h', upLinkData[6:8])[0]
            self.receivedDataDict["Depth"] = struct.unpack('f', upLinkData[8:12])[0]

            # Zip upLinkData with self.receivedDataTags to create dict and merge with self.receivedDataDict
            self.autoState(self.receivedDataDict["Auto"])

            self.lcdUpdater()
        except queue.Empty:
            print("qUplink is empty")
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
class PidMenuBack(QtWidgets.QTabWidget, pidMenu.Ui_pidMenu):
    def __init__(self, qPid):
        QtWidgets.QTabWidget.__init__(self)
        self.qPid = qPid
        self.setupUi(self)
        self.setFixedSize(645, 715)
        self.jsonData = None
        self.jsonPid = None
        self.PIDApply.clicked.connect(self.applyFunction)

        self.pidcValues = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.pidcTags = ["Roll P", "Roll I", "Roll D",
                         "Depth P", "Depth I", "Depth D",
                         "Pitch P", "Pitch I", "Pitch D",]

        self.pidcObjects = [self.roll_P, self.roll_I, self.roll_D,
                            self.depth_P, self.depth_I, self.depth_D,
                            self.pitch_P, self.pitch_I, self.pitch_D]



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
        print("jsonloadergiris")
        f = open("../CodeFiles/dataBase.json", "r")
        self.jsonData = json.load(f)
        self.jsonPid = self.jsonData["pidMenu"]
        f.close()
        for i in range(9):
            self.pidcValues[i] = self.jsonPid[self.pidcTags[i]]
        print("jsonloaderbitis")    

    def jsonDumper(self):  # Dump all of the data to the json database
        print("jsondumpergiris")
        self.getFromScreen()
        zipper = zip(self.pidcTags, self.pidcValues)
        jsonSave = dict(zipper)
        jsonSave = {"pidMenu": jsonSave}
        self.jsonData.update(jsonSave)
        f = open("/home/casmarine/GUI_MU/HighLevel-Station/CodeFiles/dataBase.json", "w")
        json.dump(self.jsonData, f, separators=(" , ", ":"), indent=4)
        f.close()
        print("jsondumperbitis")

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

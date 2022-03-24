from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QRunnable, QThreadPool, QObject
import queue
import numpy as np
import CASMarineVIII, pidMenu, thrustMenu, taskSwitchMenu, ImageSource, collections, datetime, cv2, json, socket, struct
import time
import photomosaic
#import Photomosaic2022V5
import photomosaic_main
frame = np.ndarray

# import mission2cam

PMClass = photomosaic.Photomosaic()  # Using mission 3 AND taking Task 4 bit (TLDR; Task 3 and 4 connected to this)


# Thrust, Task, PID, haberleşmeye,
# Button, Uplink arayüze gönderilecek.
class signalClass(QObject):
    change_pixmap_signal = pyqtSignal(np.ndarray)


# noinspection PyUnresolvedReferences
class VideoThread(QRunnable):
    def __init__(self, host="192.168.1.30", port=12348, cam_name=str):
        super().__init__()
        self.signals = signalClass()
        self._run_flag = True
        self._pause_flag = True
        self.MAX_DGRAM = 2 ** 16
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.cam_name = cam_name
        self.img = None
        self._mission1 = False
        self._mission2 = False
        self._mission3 = False
        self._task_bit_four = 0
        self.camJpg = cv2.imread("../Static Images/cam_icon.jpeg")
        # print(self.cam_name + " bekleniyor...")

    def dump_buffer(self):
        while self._run_flag:
            try:
                seg, addr = self.s.recvfrom(self.MAX_DGRAM)
                if struct.unpack("B", seg[0:1])[0] == 1:
                    break
            except:
                pass

    def main_loop(self):
        while not self._pause_flag and not self._mission1 and not self._mission2 and not self._mission3:
            try:
                seg, addr = self.s.recvfrom(self.MAX_DGRAM)
                if struct.unpack("B", seg[0:1])[0] > 1:
                    self.dat += seg[1:]
                else:
                    self.dat += seg[1:]
                    if ((self.dat[0] == 255) & (self.dat[1] == 216) & (self.dat[-2] == 255) & (self.dat[-1] == 217)):
                        self.img = cv2.imdecode(np.frombuffer(self.dat, dtype=np.uint8), 1)
                        self.img = cv2.flip(self.img, 2)
                        dt = time.time() - self.startTime
                        self.startTime = time.time()
                        self.dtav = .9 * self.dtav + .1 * dt
                        fps = 1 / self.dtav
                        fps = int(fps)
                        cv2.rectangle(self.img, (0, 0), (90, 40), (30, 90, 30), -1)
                        cv2.putText(self.img, str(round(fps, 1)) + ' fps', (0, 25), self.font, .75, (0, 0, 0), 2)
                        self.signals.change_pixmap_signal.emit(self.img)
                    self.dat = b''
            except:
                pass

    def mission1_loop(self):
        while not self._pause_flag and self._mission1 and not self._mission2 and not self._mission3:
            try:
                seg, addr = self.s.recvfrom(self.MAX_DGRAM)
                if struct.unpack("B", seg[0:1])[0] > 1:
                    self.dat += seg[1:]
                else:
                    self.dat += seg[1:]
                    if ((self.dat[0] == 255) & (self.dat[1] == 216) & (self.dat[-2] == 255) & (self.dat[-1] == 217)):
                        self.img = cv2.imdecode(np.frombuffer(self.dat, dtype=np.uint8), 1)
                        self.img = cv2.putText(self.img, "Mission 1", (100, 100), self.font, 0.75, (0, 0, 0), 2)
                        self.signals.change_pixmap_signal.emit(self.img)
                    self.dat = b''
            except:
                pass

    def mission2_loop(self):
        while not self._pause_flag and not self._mission1 and self._mission2 and not self._mission3:
            try:
                seg, addr = self.s.recvfrom(self.MAX_DGRAM)
                if struct.unpack("B", seg[0:1])[0] > 1:
                    self.dat += seg[1:]
                else:
                    self.dat += seg[1:]
                    if ((self.dat[0] == 255) & (self.dat[1] == 216) & (self.dat[-2] == 255) & (self.dat[-1] == 217)):
                        self.img = cv2.imdecode(np.frombuffer(self.dat, dtype=np.uint8), 1)
                        self.img = cv2.putText(self.img, "Mission 2", (100, 100), self.font, 0.75, (0, 0, 0), 2)
                        # self.img = mission2cam.main(self.img)
                        self.signals.change_pixmap_signal.emit(self.img)
                    self.dat = b''
            except:
                pass

    def mission3_loop(self):
        while not self._pause_flag and not self._mission1 and not self._mission2 and self._mission3:
            try:
                seg, addr = self.s.recvfrom(self.MAX_DGRAM)
                if struct.unpack("B", seg[0:1])[0] > 1:
                    self.dat += seg[1:]
                else:
                    self.dat += seg[1:]
                    if ((self.dat[0] == 255) & (self.dat[1] == 216) & (self.dat[-2] == 255) & (self.dat[-1] == 217)):
                        self.img = cv2.imdecode(np.frombuffer(self.dat, dtype=np.uint8), 1)
                        returned_image = PMClass.photomosaic(self.img, button=self._task_bit_four)
                        # _task_bit_four is defined in __init__ of video thread
                        # That value is changed in com function of CASMarine8 class
                        # Do not touch
                        self.signals.change_pixmap_signal.emit(returned_image)
                    self.dat = b''
            except:
                pass

    def run(self):
        cap= cv2.VideoCapture(0)
        while True:
            global frame
            ret,frame = cap.read()
        # connect = 0
        # while self._run_flag:
        #     if not self._pause_flag:
        #         try:
        #             self.s.bind((self.host, self.port))
        #             print(self.cam_name + " bağlantısı kuruldu.")
        #             break
        #         except:
        #             if connect == 0:
        #                 print(self.cam_name + " ile bağlantı kurulamadı.")
        #                 connect = 1
        #     else:
        #         time.sleep(0.01)
        #
        # self.dat = b''
        # self.dump_buffer()
        # self.font = cv2.FONT_HERSHEY_SIMPLEX
        # self.startTime = time.time()
        # self.dtav = 0
        #
        # while self._run_flag:
        #     self.main_loop()
        #     self.mission1_loop()
        #     self.mission2_loop()
        #     self.mission3_loop()
        #     # print("Thread uyuyo ses yapma")
        #     if self._pause_flag:

            self.signals.change_pixmap_signal.emit(frame)
        #     time.sleep(0.5)

        self.s.close()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._pause_flag = True
        self._run_flag = False
        # self.wait()


# noinspection PyUnresolvedReferences
class CASMarine8(QtWidgets.QMainWindow, CASMarineVIII.Ui_MainWindow):
    def __init__(self, qUplink, qPid, qThrust, qButton, qTask):
        QtWidgets.QMainWindow.__init__(self)
        self.now = None
        self.string = None
        self.setupUi(self)
        self.clKiller = collections.deque(maxlen=1)
        self.pidwin = PidMenuBack(qPid)  # qPid Values are sent in Pid menu backend class (line : 273, 348)
        self.pidwin.jsonLoader()
        self.pidwin.transmitData()
        self.thrwin = ThrustMenuBack(qThrust)  # qThrust are sent in Thrust menu backend class (line : 549, 590)
        self.thrwin.jsonLoader()
        self.thrwin.transmitData()
        self.taskwin = TaskSwitchMenuBack()
        self.taskwin.jsonLoader()
        self.buttonConfiguration = self.taskwin.taskSwitchValues
        self.activeButtonIndex = list()  # This is for starting an example list
        self.transmitData = [1, 0, 1, 0, 1, 0, 1, 0]  # This is for starting an example list
        self.stopwatchLcd.display("0:0.00")
        self.qUplink = qUplink
        self.qButton = qButton
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

        self.thread = VideoThread(port=12346, cam_name="Ön Kamera")
        self.thread.signals.change_pixmap_signal.connect(self.update_image)
        self.cameraOneCheck.stateChanged.connect(self.cameraOneState)
        self.threadPool.start(self.thread)

        # self.thread2 = VideoThread(port=12348, cam_name="Alt Kamera")
        # self.thread2.signals.change_pixmap_signal.connect(self.update_imageTwo)
        # self.cameraTwoCheck.stateChanged.connect(self.cameraTwoState)
        # self.threadPool.start(self.thread2)
        #
        # self.thread3 = VideoThread(port=12350, cam_name="Mikrorov Kamerası")
        # self.thread3.signals.change_pixmap_signal.connect(self.update_microRov)
        # self.cameraMicroCheck.stateChanged.connect(self.cameraMicroState)
        # self.threadPool.start(self.thread3)

        self.pidMenu.clicked.connect(self.pidWindow)
        self.buttonMenu.clicked.connect(self.taskSwitchWindow)
        self.thrustMenu.clicked.connect(self.thrustWindow)
        self.pushButton_screenshot.clicked.connect(self.screenShot)


        # This holds comm values in a dictionary for ease of use, bottom has tags required for zip
        self.receivedDataDict = {"Pressure": 15, "Temperature": 20, "Depth": 2,
                                 "Head": 110, "Pitch": 14, "Roll": 5, "Auto": False}
        self.receivedDataTags = ["Pressure", "Temperature", "Depth", "Head", "Pitch", "Roll", "Auto"]

        self.rot = ImageSource.Rotator()  # This is for visualizing angle values this class has required functions

        # These codes hold memory value for fast changing of autonomous light value
        self.autoLightOff = cv2.imread("../Static Images/AutoOffline.jpg")
        self.autoLightOff = self.convert_cv_qt(self.autoLightOff, horizontal=1450, vertical=20)
        self.autoLightOn = cv2.imread("../Static Images/AutoOnline.jpg")
        self.autoLightOn = self.convert_cv_qt(self.autoLightOn, horizontal=1450, vertical=20)

        self.angleImageUpdater()  # This initiates angle image visualizer

        self.dataSignalDelay = QTimer()  # This timer is for communication delay
        self.dataSignalDelay.timeout.connect(self.communicate)  # Communicate function line : 204
        self.dataSignalDelay.start(20)  # This is communication function transmission speed

        self.lcd_list = list()

    def closeEvent(self, event):
        self.thread.stop()
        self.thread2.stop()
        self.thread3.stop()
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

    @pyqtSlot(np.ndarray)
    def update_microRov(self, image):
        qtImage = self.convert_cv_qt(image)
        self.camMicro.setPixmap(qtImage)

    def cameraMicroState(self):
        if self.cameraMicroCheck.isChecked():
            self.thread3._pause_flag = False
        elif not self.cameraMicroCheck.isChecked():
            self.thread3._pause_flag = True

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

    def thrustWindow(self):
        self.thrwin.show()


    def screenShot(self):
        global frame
        photomosaic_main.wreck(frame)
        print("Tiklandı")

    def taskSwitchWindow(self):
        self.taskwin.show()

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
            self.angleImageUpdater(self.receivedDataDict["Roll"], -1 * self.receivedDataDict["Pitch"])
        except queue.Empty:
            pass

        try:  # Button que get command and create appropiate task que data
            binaryButton = self.qButton.get(timeout=0.00001)
            # print(binaryButton)
            self.activeButtonIndex = list()
            for i in range(8):
                if binaryButton & 0b00000001:
                    self.activeButtonIndex.append(i)
                binaryButton = binaryButton >> 1
            for listIndex, buttonIndex in enumerate(self.activeButtonIndex):
                self.activeButtonIndex[listIndex] = self.buttonConfiguration[buttonIndex]
            self.transmitData = list(1 if i in self.activeButtonIndex else 0 for i in range(9))
            self.transmitData = self.transmitData[1:]
        except queue.Empty:
            pass

        try:  # Task que send command
            task_array = 0b00000000
            # print(self.transmitData)
            if self.transmitData[4] + self.transmitData[5] + self.transmitData[6] > 1:
                self.transmitData[4:7] = [0, 0, 0]
                if self.thread._mission1 or self.thread._mission2 or self.thread._mission3:
                    self.thread._mission1 = False
                    self.thread._mission2 = False
                    self.thread._mission3 = False
            elif self.transmitData[4] == 1 and self.thread._mission1 == False:
                self.thread._mission1 = True
            elif self.transmitData[4] == 0 and self.thread._mission1 == True:
                self.thread._mission1 = False
            elif self.transmitData[5] == 1 and self.thread._mission2 == False:
                self.thread._mission2 = True
            elif self.transmitData[5] == 0 and self.thread._mission2 == True:
                self.thread._mission2 = False
            elif self.transmitData[6] == 1 and self.thread._mission3 == False:
                self.thread._mission3 = True
            elif self.transmitData[6] == 0 and self.thread._mission3 == True:
                self.thread._mission3 = False
            else:
                pass

            if self.transmitData[7]:  # Do not touch this photomosaic class is configured for this operation
                self.thread._task_bit_four = 1
            elif not self.transmitData[7]:
                self.thread._task_bit_four = 0

            for i in range(len(self.transmitData)):
                task_array >>= 1
                data = self.transmitData[i]
                task_array = task_array | (data * 128)
            # print(task_array)
            self.qTask.put(task_array, timeout=0.00001)
        except queue.Full:
            pass

    def lcdUpdater(self):
        self.pressureLcd.display(self.receivedDataDict["Pressure"])
        self.temperatureLcd.display(self.receivedDataDict["Temperature"])
        self.depthLcd.display(self.receivedDataDict["Depth"])
        self.headLcd.display(self.receivedDataDict["Head"])
        self.pitchLcd.display(self.receivedDataDict["Pitch"])
        self.rollLcd.display(self.receivedDataDict["Roll"])

    def angleImageUpdater(self, angleArka=0, angleYan=0):
        arkaImg = self.rot.getRotated("Arka", angleArka)
        yanImg = self.rot.getRotated("Yan", angleYan)
        arkaImg = self.convert_cv_qt(arkaImg, horizontal=200, vertical=200)
        yanImg = self.convert_cv_qt(yanImg, horizontal=200, vertical=200)
        self.angleBack.setPixmap(arkaImg)
        self.angleSide.setPixmap(yanImg)

    def autoState(self, state=False):
        if state:
            self.autoLight.setPixmap(self.autoLightOn)
        elif not state:
            self.autoLight.setPixmap(self.autoLightOff)


# noinspection PyUnresolvedReferences,PyTypeChecker
class PidMenuBack(QtWidgets.QTabWidget, pidMenu.Ui_pidMenu):
    def __init__(self, qPid):
        QtWidgets.QTabWidget.__init__(self)
        self.qPid = qPid  # Communication line : 339
        self.setupUi(self)
        self.setFixedSize(550, 700)
        self.currentChanged.connect(self.tabChange)
        self.jsonData = None
        self.jsonPid = None
        self.PIDApply.clicked.connect(self.applyFunction)
        self.servoApply.clicked.connect(self.applyFunction)
        self.pidcValues = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 0, 0, 0]
        self.pidcTags = ["Roll P", "Roll I", "Roll D", "Roll C",
                         "Depth P", "Depth I", "Depth D", "Depth C",
                         "Dir P", "Dir I", "Dir D", "Dir C",
                         "Pitch P", "Pitch I", "Pitch D", "Pitch C",
                         "Motor Speed", "Bottom Speed", "Head Speed",
                         "Camera Servo Min", "Camera Servo Max", "Gripper Min", "Gripper Max",
                         "Slider 1 Choice", "Slider 2 Choice", "Slider 3 Choice"]
        self.pidcObjects = [self.roll_P, self.roll_I, self.roll_D, self.roll_C,
                            self.depth_P, self.depth_I, self.depth_D, self.depth_C,
                            self.dir_P, self.dir_I, self.dir_D, self.dir_C,
                            self.pitch_P, self.pitch_I, self.pitch_D, self.pitch_C,
                            self.motor_Motor, self.motor_Bottom, self.motor_Head,
                            self.camServ_min, self.camServ_max, self.grip_min, self.grip_max]
        for i in range(len(self.pidcObjects)):
            self.pidcObjects[i].setValidator(QtGui.QIntValidator(0, 255))

        self.timer = QTimer()
        self.timer.timeout.connect(self.dataExchange)
        self.slider1Check.stateChanged.connect(self.timerConfig)
        self.slider2Check.stateChanged.connect(self.timerConfig)
        self.slider3Check.stateChanged.connect(self.timerConfig)
        self.sliderTags = ["None", "Roll P", "Roll I", "Roll D",
                           "Depth P", "Depth I", "Depth D",
                           "Dir P", "Dir I", "Dir D",
                           "Pitch P", "Pitch I", "Pitch D"]
        self.slider1Choice.addItems(self.sliderTags)
        self.slider2Choice.addItems(self.sliderTags)
        self.slider3Choice.addItems(self.sliderTags)
        self.lastChoiceIndex = [None, None, None]

    def tabChange(self):
        if self.currentIndex() == 0:
            self.setFixedSize(550, 700)
        elif self.currentIndex() == 1:
            self.setFixedSize(420, 330)

    def printToScreen(self):
        for i in range(23):
            self.pidcObjects[i].setText(f"{self.pidcValues[i]}")
        self.slider1Choice.setCurrentIndex(self.pidcValues[23])
        self.slider2Choice.setCurrentIndex(self.pidcValues[24])
        self.slider3Choice.setCurrentIndex(self.pidcValues[25])

    def getFromScreen(self):
        for i in range(23):
            self.pidcValues[i] = int(self.pidcObjects[i].text())
        self.pidcValues[23] = self.sliderTags.index(self.slider1Choice.currentText())
        self.pidcValues[24] = self.sliderTags.index(self.slider2Choice.currentText())
        self.pidcValues[25] = self.sliderTags.index(self.slider3Choice.currentText())

    def applyFunction(self):
        self.getFromScreen()
        self.transmitData()

    def transmitData(self):
        data = self.pidcValues[0:23]
        data[4:8], data[8:12], data[12:16] = data[12:16], data[4:8], data[8:12]
        data[1], data[2], data[5], data[6], data[9], data[10], data[13], data[14] = data[2], data[1], data[6], data[5], \
                                                                                    data[10], data[9], data[14], data[
                                                                                        13]
        data[16:23] = data[21], data[22], data[19], data[20], data[16], data[17], data[18]
        data = bytearray(data)
        try:
            self.qPid.put(data, timeout=0.00001)
        except:
            pass

    def dataExchange(self):
        if self.slider1Check.isChecked():
            choice = self.slider1Choice.currentText()
            if self.sliderTags.index(choice) > 0:
                choiceIndex = self.pidcTags.index(choice)
                if self.lastChoiceIndex[0] is not None and self.lastChoiceIndex[0] != choiceIndex:
                    self.pidcObjects[self.lastChoiceIndex[0]].setReadOnly(False)
                self.lastChoiceIndex[0] = choiceIndex
                self.pidcObjects[choiceIndex].setReadOnly(True)
                self.pidcObjects[choiceIndex].setText(str(self.slider1.value()))
        else:
            if self.lastChoiceIndex[0] is not None:
                self.pidcObjects[self.lastChoiceIndex[0]].setReadOnly(False)

        if self.slider2Check.isChecked():
            choice = self.slider2Choice.currentText()
            if self.sliderTags.index(choice) > 0:
                choiceIndex = self.pidcTags.index(choice)
                if self.lastChoiceIndex[1] is not None and self.lastChoiceIndex[1] != choiceIndex:
                    self.pidcObjects[self.lastChoiceIndex[1]].setReadOnly(False)
                self.lastChoiceIndex[1] = choiceIndex
                self.pidcObjects[choiceIndex].setReadOnly(True)
                self.pidcObjects[choiceIndex].setText(str(self.slider2.value()))
        else:
            if self.lastChoiceIndex[1] is not None:
                self.pidcObjects[self.lastChoiceIndex[1]].setReadOnly(False)

        if self.slider3Check.isChecked():
            choice = self.slider3Choice.currentText()
            if self.sliderTags.index(choice) > 0:
                choiceIndex = self.pidcTags.index(choice)
                if self.lastChoiceIndex[2] is not None and self.lastChoiceIndex[2] != choiceIndex:
                    self.pidcObjects[self.lastChoiceIndex[2]].setReadOnly(False)
                self.lastChoiceIndex[2] = choiceIndex
                self.pidcObjects[choiceIndex].setReadOnly(True)
                self.pidcObjects[choiceIndex].setText(str(self.slider3.value()))
        else:
            if self.lastChoiceIndex[2] is not None:
                self.pidcObjects[self.lastChoiceIndex[2]].setReadOnly(False)

        self.transmitData()

    def timerConfig(self):
        if self.slider1Check.isChecked() or self.slider2Check.isChecked() or self.slider3Check.isChecked():
            if not self.timer.isActive():
                self.timer.start(2)
        else:
            for i in self.lastChoiceIndex:
                if i is not None:
                    self.pidcObjects[i].setReadOnly(False)
            self.timer.stop()

    def show(self):
        QtWidgets.QTabWidget.show(self)
        self.jsonLoader()
        self.printToScreen()
        self.transmitData()

    def jsonLoader(self):
        f = open("dataBase.json", "r")
        self.jsonData = json.load(f)
        self.jsonPid = self.jsonData["pidMenu"]
        f.close()
        for i in range(26):
            self.pidcValues[i] = self.jsonPid[self.pidcTags[i]]

    def jsonDumper(self):  # Dump all of the data to the json database
        self.jsonLoader()  # This is for checking if other data (thruster, button conf) changed
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


class TaskSwitchMenuBack(QtWidgets.QWidget, taskSwitchMenu.Ui_taskMenu):  # No external comm here
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        self.setFixedSize(400, 410)
        self.TaskApply.clicked.connect(self.applyFunction)
        self.jsonTaskSwitch = None
        self.jsonData = None
        self.taskSwitchValues = [0, 0, 0, 0, 0, 0, 0, 0]
        self.taskSwitchTags = ["Button 1", "Button 2", "Button 3", "Button 4",
                               "Switch 1", "Switch 2", "Switch 3", "Switch 4"]
        self.buttonList = ["None", "Gripper", "Gripper Açı", "Kamera", "Micro ROV Kontrol ve Gripper", "Task 1",
                           "Task 2", "Task 3", "Task 8",
                           "Task 9", "Task 10", "Task 11", "Task 12", "Task 13", "Task 14", "Task 15", "Task 16"]
        self.switchList = ["None", "Gripper", "Gripper Açı", "Kamera", "Micro ROV Kontrol ve Gripper", "Task 1",
                           "Task 2", "Task 3", "Task 8",
                           "Task 9", "Task 10", "Task 11", "Task 12", "Task 13", "Task 14", "Task 15", "Task 16"]
        self.buttonObjects = [self.button_1, self.button_2, self.button_3, self.button_4]
        self.switchObjects = [self.switch_1, self.switch_2, self.switch_3, self.switch_4]
        for i in range(len(self.buttonObjects)):
            self.buttonObjects[i].addItems(self.buttonList)
        for i in range(len(self.switchObjects)):
            self.switchObjects[i].addItems(self.switchList)

    def printToScreen(self):
        for i in range(len(self.buttonObjects)):
            self.buttonObjects[i].setCurrentText(self.buttonList[self.taskSwitchValues[i]])
        for i in range(len(self.switchObjects)):
            self.switchObjects[i].setCurrentText(self.switchList[self.taskSwitchValues[i + len(self.buttonObjects)]])

    def getFromScreen(self):
        for i in range(len(self.buttonObjects)):
            t = self.buttonObjects[i].currentText()
            self.taskSwitchValues[i] = self.buttonList.index(t)
        for i in range(len(self.switchObjects)):
            t = self.switchObjects[i].currentText()
            self.taskSwitchValues[i + len(self.buttonObjects)] = self.switchList.index(t)

    def applyFunction(self):
        self.getFromScreen()
        # print(self.taskSwitchValues)
        self.transmitData()

    def transmitData(self):
        pass

    def show(self):
        QtWidgets.QWidget.show(self)
        self.jsonLoader()
        self.printToScreen()
        self.transmitData()

    def jsonLoader(self):
        f = open("dataBase.json", "r")
        self.jsonData = json.load(f)
        self.jsonTaskSwitch = self.jsonData["taskSwitchMenu"]
        f.close()
        for i in range(len(self.taskSwitchTags)):
            self.taskSwitchValues[i] = int(self.jsonTaskSwitch[self.taskSwitchTags[i]])

    def jsonDumper(self):
        self.jsonLoader()
        self.getFromScreen()
        zipper = zip(self.taskSwitchTags, self.taskSwitchValues)
        jsonSave = dict(zipper)
        jsonSave = {"taskSwitchMenu": jsonSave}
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
            self.jsonTaskSwitch = None
            event.accept()
        elif box.clickedButton() == buttonY:
            self.jsonDumper()
            self.jsonData = None
            self.jsonTaskSwitch = None
            event.accept()
        else:
            event.ignore()


class ThrustMenuBack(QtWidgets.QWidget, thrustMenu.Ui_ThrustMenu):
    def __init__(self, qThrust):
        QtWidgets.QWidget.__init__(self)
        self.qThrust = qThrust  # Communication line : 587
        self.setupUi(self)
        self.setFixedSize(400, 550)
        self.ThrustApply.clicked.connect(self.applyFunction)
        self.jsonData = None
        self.jsonThrust = None
        self.thrustValues = [0, 0, 0, 0, 0, 0, 0, 0]  # 0 is CW 1 is CCW
        self.thrustCWObjects = [self.motor1CW, self.motor2CW, self.motor3CW, self.motor4CW,
                                self.motor5CW, self.motor6CW, self.motor7CW, self.motor8CW]
        self.thrustCCWObjects = [self.motor1CCW, self.motor2CCW, self.motor3CCW, self.motor4CCW,
                                 self.motor5CCW, self.motor6CCW, self.motor7CCW, self.motor8CCW]
        self.thrustTags = ["Motor 1", "Motor 2", "Motor 3", "Motor 4", "Motor 5", "Motor 6", "Motor 7", "Motor 8"]

    def printToScreen(self):
        for i in range(8):
            if self.thrustValues[i] == 0:
                self.thrustCWObjects[i].setChecked(True)
            elif self.thrustValues[i] == 1:
                self.thrustCCWObjects[i].setChecked(True)
            else:
                pass

    def getFromScreen(self):
        for i in range(8):
            if self.thrustCWObjects[i].isChecked():
                self.thrustValues[i] = 0
            elif self.thrustCCWObjects[i].isChecked():
                self.thrustValues[i] = 1
            else:
                pass

    def applyFunction(self):
        self.getFromScreen()
        self.transmitData()

    def transmitData(self):
        data = 0b00000000
        for i in range(len(self.thrustValues)):
            data >>= 1
            bit = self.thrustValues[i]
            data = data | (bit * 128)

        try:
            self.qThrust.put(data, timeout=0.00001)
        except:
            pass

    def show(self):
        QtWidgets.QWidget.show(self)
        self.jsonLoader()
        self.printToScreen()
        self.transmitData()

    def jsonLoader(self):
        f = open("dataBase.json", "r")
        self.jsonData = json.load(f)
        self.jsonThrust = self.jsonData["thrustMenu"]
        f.close()
        for i in range(8):
            self.thrustValues[i] = int(self.jsonThrust[self.thrustTags[i]])

    def jsonDumper(self):
        self.jsonLoader()
        self.getFromScreen()
        zipper = zip(self.thrustTags, self.thrustValues)
        jsonSave = dict(zipper)
        jsonSave = {"thrustMenu": jsonSave}
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
            self.jsonThrust = None
            event.accept()
        elif box.clickedButton() == buttonY:
            self.jsonDumper()
            self.jsonData = None
            self.jsonThrust = None
            event.accept()
        else:
            event.ignore()

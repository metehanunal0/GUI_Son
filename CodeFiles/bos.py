from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QTimer, QRunnable, QThreadPool, QObject
import queue
from multiprocessing import Queue
import numpy as np
import casmarine8_10_1, pidMenu, collections, datetime, cv2, json, socket, struct
import time
import photomosaic_main
from missionMenu import *
from pidMenu import PidMenuBack


# import mission2cam
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

    def main_loop(self):  ############### MISSIONLAR ????? ###### SİLİM Mİ?
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
        connect = 0
        while self._run_flag:
            if not self._pause_flag:
                try:
                    self.s.bind((self.host, self.port))
                    print(self.cam_name + " bağlantısı kuruldu.")
                    break
                except:
                    if connect == 0:
                        print(self.cam_name + " ile bağlantı kurulamadı.")
                        connect = 1
            else:
                time.sleep(0.01)

        self.dat = b''
        self.dump_buffer()
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.startTime = time.time()
        self.dtav = 0

        while self._run_flag:
            self.main_loop()
            self.mission1_loop()
            self.mission2_loop()
            self.mission3_loop()
            # print("Thread uyuyo ses yapma")
            if self._pause_flag:
                self.signals.change_pixmap_signal.emit(self.camJpg)
            time.sleep(0.5)

        self.s.close()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._pause_flag = True
        self._run_flag = False
        # self.wait()


# noinspection PyUnresolvedReferences
class CASMarine8(QtWidgets.QMainWindow, casmarine8_10_1.Ui_MainWindow):  # qButton?
    def __init__(self, qUplink, qPid, qTask):
        QtWidgets.QMainWindow.__init__(self)
        self.now = None
        self.string = None
        self.setupUi(self)
        self.clKiller = collections.deque(maxlen=1)
        self.pidwin = PidMenuBack(qPid)  # qPid Values are sent in Pid menu backend class (line : 273, 348)
        self.pidwin.jsonLoader()
        self.pidwin.transmitDatav2()

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

        self.thread = VideoThread(port=12346, cam_name="Ön Kamera")
        self.thread.signals.change_pixmap_signal.connect(self.update_image)
        self.cameraOneCheck.stateChanged.connect(self.cameraOneState)
        self.threadPool.start(self.thread)

        self.thread2 = VideoThread(port=12348, cam_name="Alt Kamera")
        self.thread2.signals.change_pixmap_signal.connect(self.update_imageTwo)
        self.cameraTwoCheck.stateChanged.connect(self.cameraTwoState)
        self.threadPool.start(self.thread2)

        self.pidMenu.clicked.connect(self.pidWindow)
        self.pushButton_screenshot.clicked.connect(self.screenShot)
        self.mission_object = InitializeMissionMenu()
        self.missionMenu.clicked.connect(self.missionWindow)
        self.mission_object.mission_signal.connect(self.selectMission)

        # This holds comm values in a dictionary for ease of use, bottom has tags required for zip
        self.receivedDataDict = {"Pressure": 15, "Depth": 2,
                                 "Head": 110, "Pitch": 14, "Roll": 5, "Auto": False}
        self.receivedDataTags = ["Pressure", "Depth", "Head", "Pitch", "Roll", "Auto"]

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

    def selectMission(self, mission):  # değişcek
        print("fonks girdi ")
        if mission == "Mission-1":
            self.mission_1()
        elif mission == "Mission-2":
            self.mission_2()
        elif mission == "Mission-3":
            self.mission_3()
        elif mission == "Mission-4":
            self.mission_4()
        elif mission == "Mission-5":
            self.mission_5()
        else:
            print("Görevlere girmedi mq")

    def mission_1(self):
        print("Görev-1 mq")

    def mission_2(self):
        print("Görev-2 mq")

    def mission_3(self):
        print("Görev-3 mq")

    def mission_4(self):
        print("Görev-4 mq")

    def mission_5(self):
        print("Görev-5 mq")

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

    def screenShot(self, qFrameIn: Queue):  # HATA
        # haberleşme lazım qFrameIn
        photomosaic_main.wreck(qFrameIn)  # hata

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
            # self.angleImageUpdater(self.receivedDataDict["Roll"], -1 * self.receivedDataDict["Pitch"])             # BU NEDİR? NE İŞE YARAMAKTADIR?
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


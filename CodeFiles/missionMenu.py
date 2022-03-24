from missionMenuFace import Ui_missionMenu
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

class InitializeMissionMenu(QWidget):
    mission_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.ui = Ui_missionMenu()
        self.ui.setupUi(self)
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(["Mission-1","Mission-2","Mission-3","Mission-4","Mission-5","Mission-6"])
        self.ui.applyButton.clicked.connect(self.goSignal)


    def goSignal(self):
        selected_mission = self.ui.comboBox.currentIndex()
        #print(type(selected_mission))
        self.mission_signal.emit(selected_mission)

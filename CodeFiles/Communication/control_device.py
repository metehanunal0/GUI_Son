"""
-> Implementation of a Joystick and Gamepad class
These classes' methods outputs the position values of
all axes of a control device, and sends it in
bytearray format as the input of control algorithms.
@Authors    = Furkan Kirlangic, Zeynep Yurttaş
@Date       = 30.01.22
@Update     = 14.03.22
"""

from matplotlib.pyplot import axis
from pygame import joystick, event, display
from multiprocessing import Process, Queue
from time import sleep

"""
GAMEPAD CLASS
"""


class Gamepad():
    def __init__(self):
        print("Waiting for init")
        while True:
            joystick.init()
            if joystick.get_init() and joystick.get_count() == 1:
                id = joystick.get_count() - 1
                display.init()
                self.gamepad = joystick.Joystick(id)
                self.gamepad.init()
                if self.gamepad.get_init():
                    print("Gamepad connected")
                    break
            else:
                print("Init failed")
                joystick.quit()

        # Get number of axis and button from gamepad
        self.numaxes = self.gamepad.get_numaxes()
        self.numbuttons = self.gamepad.get_numbuttons()
        self.q_size = 50
        self.q = Queue(self.q_size)

        "---------- AXIS AND BUTTON IDS ----------"
        self.axis_map = {
            "X": 0,
            "Y": 1,
            "HEAD": 3,
            "Z": 4
        }
        self.buttons_map = {
            "A": 0,
            "B": 1,
            "X": 2,
            "Y": 3,
            "LB": 4,
            "RB": 5,
            "BACK": 6,
            "START": 7
        }
        self.id_map = (self.axis_map, self.buttons_map)

    def send_control_data(self) -> None:
        """
        @definition: Calculate axis values and put in a queue.
        """
        while True:
            event.pump()
            axis_data = [self.get_axis_value(axis_id) for _, axis_id in self.axis_map.items()]
            try:
                # print(axis_data)
                self.q.put(bytearray(axis_data))
            except:
                print('Exception: cannot put joystick input to the queue.')
            sleep(0.02)

    def get_axis_value(self, axis) -> int:
        """
        @params: axis = id number of an axis
        @return: (int) Get an axis and return it's position with the interval of [0, 255]
        """

        x = self.gamepad.get_axis(axis)
        axis_pos = (255 / 2) * (x + 1)
        axis_pos = round(axis_pos)
        assert axis_pos >= 0 and axis_pos <= 255, "axis position is out of range"
        return axis_pos

    "------------------------ ID finder functions for buttons and axes----------------------"

    def findAxes(self):
        """
        Prints axis position with id number -> tuple(axis_pos, id)
        """
        while True:
            event.pump()
            axis_data = [(self.get_axis_value(i), i) for i in range(self.numaxes)]
            print(axis_data)

    def findButtons(self):
        """
        Prints button state with id number -> tuple(button_state, id)
        """
        while True:
            event.pump()
            button_data = [(self.gamepad.get_button(i), i) for i in range(self.numbuttons)]
            print(button_data)


"""
JOYSTICK CLASS
"""


class Joystick():

    def __init__(self):
        print("Waiting for init")
        while True:
            joystick.init()
            if joystick.get_init() and joystick.get_count() == 1:
                id = joystick.get_count() - 1
                display.init()
                self.joystick = joystick.Joystick(id)
                self.joystick.init()
                if self.joystick.get_init():
                    print("Joystick connected")
                    break
            else:
                joystick.quit()

        # Get number of axis and button from gamepad
        self.numaxes = self.joystick.get_numaxes()
        self.numbuttons = self.joystick.get_numbuttons()
        self.q_size = 50
        self.q = Queue(self.q_size)

        "---------- AXIS AND BUTTON IDS ----------"
        self.axis_map = {
            "X": 0,
            "Y": 1,
            "HEAD": 2,
            "Z": 3
        }
        self.buttons_map = {
            "TRIG": 0,
            "THUMB": 1,
            "BUTTON3": 2,
            "BUTTON4": 3,
            "BUTTON5": 4,
            "BUTTON6": 5,
            "BUTTON7": 6,
            "BUTTON8": 7,
            "BUTTON9": 8,
            "BUTTON10": 9,
            "BUTTON11": 10,
            "BUTTON12": 11
        }
        self.id_map = (self.axis_map, self.buttons_map)

        self.Z_BUTTONS = {
            "BUTTON_Z_UP": self.buttons_map["TRIG"],
            "BUTTON_Z_DOWN": self.buttons_map["THUMB"]
        }
        self.Z_SPEED = {
            "NORMAL_SPEED": 128,
            "UP_SPEED": 128 + 50,
            "DOWN_SPEED": 128 - 50
        }

    def get_z_value(self) -> int:
        """
        @params: None
        @return: (int) Return the Z value within the interval of [0, 255]
        """
        if (self.joystick.get_button(self.Z_BUTTONS["BUTTON_Z_UP"]) and not self.joystick.get_button(
                self.Z_BUTTONS["BUTTON_Z_DOWN"])):
            return self.Z_SPEED["UP_SPEED"]
        elif (self.joystick.get_button(self.Z_BUTTONS["BUTTON_Z_DOWN"]) and not self.joystick.get_button(
                self.Z_BUTTONS["BUTTON_Z_UP"])):
            return self.Z_SPEED["DOWN_SPEED"]
        else:
            return self.Z_SPEED["NORMAL_SPEED"]

    def get_axis_value(self, axis) -> int:
        """
        @params: axis = id number of an axis
        @return: (int) Get an axis and return it's position with the interval of [0, 255]
        """
        x = self.joystick.get_axis(axis)
        axis_pos = (255 / 2) * (x + 1)
        axis_pos = round(axis_pos)
        assert axis_pos >= 0 and axis_pos <= 255, "axis position is out of range"
        return axis_pos

    def send_control_data(self):
        """
        @definition: Calculate axis values and put in a queue.
        """
        while True:
            event.pump()
            axis_data = [self.get_axis_value(axis_id) for key, axis_id in self.axis_map.items() if not key == "Z"] + [
                self.get_z_value()]
            axis_data = bytearray(axis_data)
            try:
                self.q.put(axis_data)
            except:
                print('Exception: cannot put joystick input to the queue.')

    "------------------------ ID finder functions for buttons and axes----------------------"

    def findAxes(self):
        """
        Prints axis position with id number -> tuple(axis_pos, id)
        """
        while True:
            event.pump()
            joystick_data = [(self.get_axis_pos(i), i) for i in range(self.numaxes)]
            print(joystick_data)

    def findButtons(self):
        """
        Prints button state with id number -> tuple(button_state, id)
        """
        while True:
            event.pump()
            button_data = [(self.joystick.get_button(i), i) for i in range(self.numbuttons)]
            print(button_data)


if __name__ == '__main__':
    js = Gamepad()
    js.send_control_data()
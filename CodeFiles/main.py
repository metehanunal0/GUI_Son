from Communication.UART import Uart
from Communication.UDP import Udp
from Communication.control_device import Gamepad
from multiprocessing import Process, Queue
import sys
from backend_CASMarineX import CASMarineX
from PyQt5.QtWidgets import *

# -------------------Create Objects----------------------------------------

# udpSend = Udp(12456, addr="192.168.1.29", client=False)
# udpRec = Udp(12455, addr="192.168.1.30", client=True)
# uartRec = Uart('/dev/ttyUSB0', baud_rate=115200, message_size=10)
camFront = Udp(port=12456, addr="localhost", client=True)
camBottom = Udp(port=4561, addr="localhost", client=True)

# gpad = Gamepad()

# -------------------Create Processes--------------------------------------
# downlink data = gamepad + button, slider (uart) + pid ---> will be sent through udp
# p1 = Process(target=gpad.send_control_data)
# p2 = Process(target=uartRec.uart_receive_validation)
# p3 = Process(target=udpSend.send_msg, args=(gpad.q, uartRec.uart_receive_queue, pid))

def interface():
    app = QApplication(sys.argv)
    ui = CASMarineX(qUplink=q1, qPid=q2, qTask=q3, qFrontCam=camFront.im_queue, qBottomCam=camBottom.im_queue)
    ui.show()
    sys.exit(app.exec_())


p1 = Process(target=camFront.get_vid_stream)
p2 = Process(target=camBottom.get_vid_stream)
p3 = Process(target=interface)

q1 = Queue()
q2 = Queue()
q3 = Queue()

proc = [p1, p2, p3]

if __name__ == "__main__":

    for p in proc:
        p.start()
    for p in proc:
        p.join()

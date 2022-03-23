"""
@Author: Furkan Kirlangic
@Last Revision: 22.12.2021
"""

import base64
import socket
from multiprocessing import Queue

import cv2
import imutils
import numpy as np
from cv2 import cv2 as cv

SIZE = 65536  # UDP data transfer size in bytes


class Udp:
    """
    If data will be sent, the device is called server.
    If client, addr is client address
    If server, addr is client address
    """

    def __init__(self, port: int, addr: str, client=False):  # client true if receiving
        self.im_queue = Queue(10)
        self.transfer_queue = Queue(10)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, SIZE)
        self.host_ip = addr
        self.port = port
        self.socket_address = (self.host_ip, self.port)

        # self.socket.bind(self.socket_address)

        if client == True:
            while True:
                try:
                    self.socket.bind(self.socket_address)
                    print("Binded successfully")
                    break
                except:
                    pass


    """                                   Video Stream                                            """
    """-------------------------------------------------------------------------------------------"""

    def vid_stream(self, width: int, height: int, im_quality: int, cam_id: int):
        cap = cv.VideoCapture(cam_id)  # device id is left zero, will be updated later when cameras are connected
        client_addr = self.socket_address
        while cap.isOpened():
            _, frame = cap.read()
            frame = imutils.resize(frame, width=width, height=height)

            encoded, buffer = cv.imencode('.jpg', frame, [cv.IMWRITE_JPEG_QUALITY, im_quality])
            message = base64.b64encode(buffer)
            try:
                self.socket.sendto(message, client_addr)
            except:

                print('Cannot send image over UDP')
            """cv.imshow('transmitting', frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                self.socket.close()
                break
            """

    def get_vid_stream(self):
        while True:
            packet, _ = self.socket.recvfrom(SIZE)
            data = base64.b64decode(packet, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)
            frame = cv.imdecode(npdata, 1)

            try:
                self.im_queue.put(frame)

                # cv2.imshow("fram", frame)
                # cv2.waitKey(0)
            except:
                print('Cannot put frame to queue')
            """cv.imshow("receiving", frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord('q'):
                self.socket.close()
                break"""

    """                                 Non-video UDP transmission                                """
    """-------------------------------------------------------------------------------------------"""

    def send_msg(self, qOut: Queue):
        while True:
            message = qOut.get()
            if type(message) != bytearray:
                message = bytearray(message)
            try:
                self.socket.sendto(message, self.socket_address)
            except:
                print('Cannot send UDP message')

    def receive_msg(self):
        while True:
            try:
                message, _ = self.socket.recvfrom(SIZE)
                if type(message) != bytearray:
                    message = bytearray(message)
                # print(list(message))
                self.transfer_queue.put(message)
            except:
                print('Cannot receive UDP message')
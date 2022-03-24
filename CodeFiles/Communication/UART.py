"""
@Author: Furkan Kirlangic
@Last Revision: 25.12.2021
"""

import serial
from crccheck.crc import Crc32Mpeg2
from concurrent.futures import ThreadPoolExecutor
from collections import deque
from multiprocessing import Queue
import time


class Uart:
    """
    If data will be sent, message_size is not important
    If data will be received, message_size is header size + data size + crc size
    """

    def __init__(self, port: str, baud_rate, message_size):
        self.port = port
        self.baud_rate = baud_rate
        self.message_size_with_header = message_size
        self.message_size = self.message_size_with_header - 2
        self.header = [4, 5]

        # Containers for data handling
        self.temp_buffer = deque(maxlen=100)
        self.uart_send_queue = Queue(100)
        self.uart_intermed_send_queue = Queue(100)
        self.uart_receive_queue = Queue(100)
        self.output = Queue(100)

        while True:
            try:
                self.ser = serial.Serial(port=self.port, baudrate=self.baud_rate)
                break
            except serial.SerialException:
                pass

        print("Connection with card established.")

    """                                 Serial Reading                                            """
    """-------------------------------------------------------------------------------------------"""

    def read_serial(self):
        while True:
            if self.ser.in_waiting >= self.message_size_with_header:
                self.temp_buffer.append(self.ser.read(self.message_size_with_header))

    def read_non_serial(self, outside_queue: Queue):
        while True:
            # print('READ NON SERIAL')
            queue_item = outside_queue.get()
            assert type(queue_item) == bytearray, "received data is not bytearray"
            crc = Crc32Mpeg2.calc(queue_item).to_bytes(4, 'big')
            # crc = [i for i in crc]
            data = bytearray(self.header) + queue_item + crc
            try:
                self.uart_send_queue.put(data)

            except:
                print('Exception: read non serial')

    def validate_data(self):
        while True:
            if len(self.temp_buffer) > 0:
                unchecked_data = self.temp_buffer.popleft()
                print(unchecked_data)
                if unchecked_data[0] == self.header[0] and unchecked_data[1] == self.header[1]:
                    # print(Crc32Mpeg2.calc(unchecked_data))
                    if Crc32Mpeg2.calc(unchecked_data[2:]) == 0x00000000:
                        final_data = unchecked_data[2:-4]
                        try:
                            self.uart_receive_queue.put(final_data)
                            print(f"Get:2 - {final_data}")
                        except:
                            print('Exception: validate_data, cannot put received data to queue')

            else:
                pass

    """                                 Serial Writing                                            """
    """-------------------------------------------------------------------------------------------"""

    def send_data(self):  # Get data packets from transfer queue and write to serial port
        queue_item_stable = [128, 128, 128, 128]
        crc = Crc32Mpeg2.calc(queue_item_stable).to_bytes(4, 'big')
        # crc = [i for i in crc]
        data = self.header + list(queue_item_stable) + list(crc)
        b_data = bytearray(data)

        while True:
            try:
                queue_item = self.uart_send_queue.get()
                if type(queue_item) != bytearray:
                    queue_item = bytearray(queue_item)
                # print(list(queue_item))
                self.ser.write(queue_item)
            except:
                self.ser.write(b_data)
                print('Exception: send_data, cannot send uart data')

    def uart_send_data(self, outside_queue: Queue):
        while True:
            queue_item = outside_queue.get()
            if type(queue_item) != bytearray:
                queue_item = bytearray(queue_item)
            crc = Crc32Mpeg2.calc(queue_item).to_bytes(4, 'big')
            # crc = [i for i in crc]
            data = self.header + list(queue_item) + list(crc)
            b_data = bytearray(data)

            try:
                # print(list(b_data))
                self.ser.write(b_data)
            except:
                print('Exception: uart_send_data')

    """                                 Concurrent Serial R/W                                     """
    """-------------------------------------------------------------------------------------------"""

    def uart_receive_validation(self):  # Read serial data and check it
        with ThreadPoolExecutor() as executor:
            executor.submit(self.read_serial, )
            executor.submit(self.validate_data, )

    def uart_send_data_th(self, outside_queue: Queue):
        with ThreadPoolExecutor() as executor:
            executor.submit(self.read_non_serial, outside_queue)
            executor.submit(self.send_data)

    def uart_send_data_nonstop(self, outside_queue: Queue):
        with ThreadPoolExecutor() as executor:
            executor.submit(self.read_non_serial, outside_queue)
            executor.submit(self.send_data_ns)
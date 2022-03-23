from CodeFiles.Communication.UDP import Udp
from multiprocessing import Process, Queue

camFront = Udp(port=12456, addr="localhost", client=False)
camBottom = Udp(port=4561, addr="localhost", client=False)

p1 = Process(target=camFront.vid_stream, args=(640, 480, 60, 0))
p2 = Process(target=camBottom.vid_stream, args=(640, 480, 60, 2))

proc = [p1, p2]

if __name__ == "__main__":
    for p in proc:
        p.start()
    for p in proc:
        p.join()

from Photomosaic2022V5 import Photomosaic
from multiprocessing import Queue, Process
import cv2
import os

photomosaic = Photomosaic()

count = 72
def wreck(qFrameIn:Queue):
    global count
    while True:
        try:
            frame = qFrameIn.get()
            photomosaic.take_photo(frame)
            count+=1
            cv2.imwrite(f'../scrShots/Frame{count}.jpg',frame)
            break
        except:
            pass


    photomosaic.filter_image()
    photomosaic.find_rect()











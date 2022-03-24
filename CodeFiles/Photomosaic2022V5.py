import cv2
import numpy as np


class Photomosaic:

    def __init__(self):
        self.cap = cv2.VideoCapture('TestVideos/test_video.mp4')
        self.frames = [np.ndarray, np.ndarray, np.ndarray, np.ndarray,
                       np.ndarray, np.ndarray, np.ndarray, np.ndarray]
        self.fr_index = 0

        self.kernel = np.ones((3, 3), np.uint8)
        self.h_kernel = np.ones((1, 20), np.uint8)
        self.pink_range = [np.array([156, 40, 155], np.uint8), np.array([179, 128, 255], np.uint8)]
        self.blue_range = [np.array([100, 120, 182], np.uint8), np.array([130, 255, 255], np.uint8)]

        self.f_img_list = []
        self.c_img_list = [np.ndarray, np.ndarray, np.ndarray, np.ndarray,
                           np.ndarray, np.ndarray, np.ndarray, np.ndarray]

        self.top_count = 0
        self.left_count = 0
        self.right_count = 0
        self.bottom_count = 0
        self.top_list = []
        self.left_list = []
        self.right_list = []
        self.bottom_list = []
        self.corner_coor = [[], [], [], []]
        self.aver_x = 0
        self.aver_y = 0

    def __call__(self):
        self.video_reader()

    def video_reader(self):
        if self.cap.isOpened() is False:
            print("Error opening video stream or file")

        while self.cap.isOpened():

            ret, frame = self.cap.read()

            if ret is True:
                frame = cv2.resize(frame, (640, 480), fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
                cv2.namedWindow('video', cv2.WINDOW_NORMAL)
                cv2.imshow('video', frame)
                key = cv2.waitKey(10)
                if key == ord('t'):
                    print('basıldı')
                    self.take_photo(frame)
                elif key == ord('q'):
                    break

            else:
                self.filter_image()
                self.find_rect()

    def take_photo(self, frame):
        if self.fr_index < 8:
            print(self.fr_index)
            self.frames[self.fr_index] = frame
            self.fr_index += 1

    def filter_image(self):
        for img in self.frames:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            cv2.imshow('img', img)
            cv2.waitKey(0)
            pink_mask = cv2.inRange(hsv, self.pink_range[0], self.pink_range[1])
            blue_mask = cv2.inRange(hsv, self.blue_range[0], self.blue_range[1])
            mask = cv2.bitwise_or(pink_mask, blue_mask)
            self.f_img_list.append(mask)

    def find_rect(self):
        for num, f in enumerate(self.f_img_list):
            width = f.shape[1]
            height = f.shape[0]
            self.top_count = 0
            self.left_count = 0
            self.right_count = 0
            self.bottom_count = 0
            lines = cv2.HoughLines(f, 1, np.pi / 180, 125)
            for line in lines:
                for rho, theta in line:
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + width * (-b))
                    y1 = int(y0 + height * (a))
                    x2 = int(x0 - width * (-b))
                    y2 = int(y0 - height * (a))
                    if abs(y2 - y1) < 50:  # Horizontal Lines
                        if y2 > height / 2:  # Bottom
                            self.bottom_list.append([0, 0, 0, 0])
                            self.bottom_list[self.bottom_count][0] = x1
                            self.bottom_list[self.bottom_count][1] = x2
                            self.bottom_list[self.bottom_count][2] = y1
                            self.bottom_list[self.bottom_count][3] = y2
                            self.bottom_count += 1
                        else:  # Top
                            self.top_list.append([0, 0, 0, 0])
                            self.top_list[self.top_count][0] = x1
                            self.top_list[self.top_count][1] = x2
                            self.top_list[self.top_count][2] = y1
                            self.top_list[self.top_count][3] = y2
                            self.top_count += 1
                    elif abs(x2 - x1) < 50:  # Vertical Lines

                        if x2 > width / 2:  # Right
                            self.right_list.append([0, 0, 0, 0])
                            self.right_list[self.right_count][0] = x1
                            self.right_list[self.right_count][1] = x2
                            self.right_list[self.right_count][2] = y1
                            self.right_list[self.right_count][3] = y2
                            self.right_count += 1
                        else:  # Left
                            self.left_list.append([0, 0, 0, 0])
                            self.left_list[self.left_count][0] = x1
                            self.left_list[self.left_count][1] = x2
                            self.left_list[self.left_count][2] = y1
                            self.left_list[self.left_count][3] = y2
                            self.left_count += 1

            top_right = [self.top_count, self.right_count, self.top_list, self.right_list]
            top_left = [self.top_count, self.left_count, self.top_list, self.left_list]
            bottom_right = [self.bottom_count, self.right_count, self.bottom_list, self.right_list]
            bottom_left = [self.bottom_count, self.left_count, self.bottom_list, self.left_list]
            corners = [top_right, top_left, bottom_right, bottom_left]
            cv2.imshow('img', self.frames[num])
            cv2.waitKey(0)
            self.crop_img(corners, f, num)
        self.show_img()

    def find_intersection(self, coor_1, coor_2):

        ax = coor_1[0]
        bx = coor_1[1]
        ay = coor_1[2]
        by = coor_1[3]
        cx = coor_2[0]
        dx = coor_2[1]
        cy = coor_2[2]
        dy = coor_2[3]

        t = ((dy - cy) * (cx - ax) - (cy - ay) * (dx - cx)) / ((dy - cy) * (bx - ax) - (by - ay) * (dx - cx))

        ex = ax + (bx - ax) * t
        ey = ay + (by - ay) * t

        self.aver_x += ex
        self.aver_y += ey

    def crop_img(self, corners, f, num):
        width = f.shape[1]
        height = f.shape[0]
        for n, cor in enumerate(corners):
            self.aver_x = 0
            self.aver_y = 0

            for i in range(cor[0]):
                for j in range(cor[1]):
                    iter_1 = cor[2][i]
                    iter_2 = cor[3][j]
                    self.find_intersection(iter_1, iter_2)
            self.corner_coor[n] = [self.aver_x / (cor[0] * cor[1]), self.aver_y / (cor[0] * cor[1])]

        pts1 = np.float32([[self.corner_coor[1][0], self.corner_coor[1][1]], [self.corner_coor[0][0], self.corner_coor[0][1]],
                           [self.corner_coor[3][0], self.corner_coor[3][1]], [self.corner_coor[2][0], self.corner_coor[2][1]]])

        pts2 = np.float32([[0, 0], [width, 0],
                           [0, height], [width, height]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        result = cv2.warpPerspective(self.frames[num], matrix, (width, height))
        self.c_img_list[num] = result

    def mosaic(self, interpolation=cv2.INTER_CUBIC):
        img_list = self.c_img_list
        h_first_row = min(img.shape[0] for img in img_list[:4])
        h_second_row = min(img.shape[0] for img in img_list[4:])
        for i in range(4):
            img = cv2.resize(img_list[i], (img_list[i].shape[1],h_first_row), interpolation=interpolation)
            img_list[i] = img
        for i in range(4):
            img = cv2.resize(img_list[i + 4], (img_list[i].shape[1],h_second_row), interpolation=interpolation)
            img_list[i + 4] = img

        w_first_row = [img.shape[1] for img in img_list[:4]]

        for i in range(4):
            img = cv2.resize(img_list[i + 4], (w_first_row[i], img_list[i + 4].shape[0]), interpolation=interpolation)
            img_list[i + 4] = img
            first_row = cv2.hconcat(img_list[:4])
            second_row = cv2.hconcat((img_list[4:]))
            sum_row = cv2.vconcat([first_row, second_row])

            return sum_row

    def show_img(self):
        for i in range(len(self.c_img_list)):
            cv2.imshow(str(i), self.c_img_list[i])
            cv2.waitKey(0)
        last_img = self.mosaic()
        cv2.namedWindow('last', cv2.WINDOW_NORMAL)
        cv2.imshow('last', last_img)
        cv2.waitKey(0)


photo = Photomosaic()
photo()

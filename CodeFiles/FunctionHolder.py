import cv2
import numpy as np


def detLen(pts0, pts1):
    xSquared = np.power((pts1[0]-pts0[0]), 2)
    ySquared = np.power((pts1[1]-pts0[1]), 2)
    return np.sqrt((xSquared+ySquared))


def getSecondImage(imageBIN, imageRAW, areaUpper=150000, areaLower=40000):

    kernel = np.ones((5, 5))
    imageDiluted = cv2.dilate(imageBIN, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(imageDiluted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours is not None:
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if areaUpper > area > areaLower:
                polyapp = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
                if len(polyapp) == 4:
                    if polyapp[0, 0, 0] <= polyapp[2, 0, 0]:
                        pts1 = np.float32([polyapp[0, 0], polyapp[1, 0], polyapp[2, 0], polyapp[3, 0]])
                        lineHorizontal = detLen(polyapp[1, 0], polyapp[0, 0])
                        lineVertical = detLen(polyapp[3, 0], polyapp[0, 0])
                    elif polyapp[0, 0, 0] > polyapp[2, 0, 0]:
                        pts1 = np.float32([polyapp[1, 0], polyapp[2, 0], polyapp[3, 0], polyapp[0, 0]])
                        lineHorizontal = detLen(polyapp[2, 0], polyapp[1, 0])
                        lineVertical = detLen(polyapp[0, 0], polyapp[1, 0])

                    if (lineHorizontal * 0.80) < lineVertical < (lineHorizontal * 1.20) or\
                            (lineVertical * 0.80) < lineHorizontal < (lineVertical * 1.20):
                        pts2 = np.float32([[0, 0], [0, 300], [300, 300], [300, 0]])
                        matrix = cv2.getPerspectiveTransform(pts1, pts2)
                        outImage = cv2.warpPerspective(imageRAW, matrix, (300, 300))
                        shapeString = "Square"
                    elif lineHorizontal > lineVertical:
                        pts2 = np.float32([[0, 300], [600, 300], [600, 0], [0, 0]])
                        matrix = cv2.getPerspectiveTransform(pts1, pts2)
                        outImage = cv2.warpPerspective(imageRAW, matrix, (600, 300))
                        shapeString = "Rectangle"
                    elif lineVertical > lineHorizontal:
                        pts2 = np.float32([[0, 0], [0, 300], [600, 300], [600, 0]])
                        matrix = cv2.getPerspectiveTransform(pts1, pts2)
                        outImage = cv2.warpPerspective(imageRAW, matrix, (600, 300))
                        shapeString = "Rectangle"
                    else:
                        outImage = np.zeros((300, 300), np.uint8)
                        shapeString = "Square"

                    return outImage, shapeString
    return None, None


def check_color_and_construct():
    imgList = [cv2.imread("../Images/Square1.jpg"), cv2.imread("../Images/Rectangle1.jpg"),
               cv2.imread("../Images/Square2.jpg"), cv2.imread("../Images/Rectangle2.jpg"),
               cv2.imread("../Images/Up.jpg")]
    imgBlackAndWhite = list(cv2.cvtColor(i, cv2.COLOR_BGR2GRAY) for i in imgList)
    maskList = []
    
    rgbMeanList = [[[0 for i in range(3)] for i in range(4)] for i in range(5)]
    rgbMeanListHSV = [[[0 for i in range(3)] for i in range(4)] for i in range(5)]
    # for image one ( indice 0) [left rgb tupple, top rgb tupple, right rgb tupple, bottom rgb tupple]
    
    # extract white from images
    for i, item in enumerate(imgBlackAndWhite):
        blur = cv2.GaussianBlur(item, (5, 5), 1)
        ret, maskWhite = cv2.threshold(blur, 165, 255, cv2.THRESH_BINARY_INV)
        ret, maskBlack = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY)
        maskBlack = cv2.erode(maskBlack, np.ones((5, 5), np.uint8), iterations=3)
        rmask = cv2.bitwise_and(maskWhite, maskBlack)
        maskList.append(rmask)
        
    # extract left side mean shape gives height width channel
    for i, item in enumerate(imgList):
        pts = np.array([(0, 0), (0, item.shape[0]), (int(item.shape[0]/2), int(item.shape[0]/2))], dtype=np.int32)
        rmask = np.zeros((item.shape[0], item.shape[1]), dtype=np.uint8)
        cv2.fillConvexPoly(rmask, pts, 255)
        leftImgMask = cv2.bitwise_and(rmask, maskList[i])
        val = cv2.mean(item, leftImgMask)
        rgbMeanList[i][0] = val[0:3]

    # extract top side
    for i, item in enumerate(imgList):
        pts = np.array([(0, 0), (item.shape[1], 0), (int(item.shape[1]/2), int(item.shape[0]/2))], dtype=np.int32)
        rmask = np.zeros((item.shape[0], item.shape[1]), dtype=np.uint8)
        cv2.fillConvexPoly(rmask, pts, 255)
        topImgMask = cv2.bitwise_and(rmask, maskList[i])
        val = cv2.mean(item, topImgMask)
        rgbMeanList[i][1] = val[0:3]

    # extract right side
    for i, item in enumerate(imgList):
        pts = np.array([(item.shape[1], item.shape[0]), (item.shape[1], 0),
                        (int(item.shape[1] - (item.shape[0] / 2)), int(item.shape[0] / 2))], dtype=np.int32)
        rmask = np.zeros((item.shape[0], item.shape[1]), dtype=np.uint8)
        cv2.fillConvexPoly(rmask, pts, 255)
        rightImgMask = cv2.bitwise_and(rmask, maskList[i])
        val = cv2.mean(item, rightImgMask)
        rgbMeanList[i][2] = val[0:3]

    # extract bottom side
    for i, item in enumerate(imgList):
        pts = np.array([(item.shape[1], item.shape[0]), (0, item.shape[0]), (int(item.shape[1] / 2), int(item.shape[0] / 2))], dtype=np.int32)
        rmask = np.zeros((item.shape[0], item.shape[1]), dtype=np.uint8)
        cv2.fillConvexPoly(rmask, pts, 255)
        bottomImgMask = cv2.bitwise_and(rmask, maskList[i])
        val = cv2.mean(item, bottomImgMask)
        rgbMeanList[i][3] = val[0:3]
    
    # change values to hsv to compare
    for i, ix in enumerate(rgbMeanList):
        for j, jx in enumerate(ix):
            colorBGR = np.zeros((1, 1, 3), np.uint8)
            colorBGR[0, 0] = int(jx[0]), int(jx[1]), int(jx[2])
            temp = cv2.cvtColor(colorBGR, cv2.COLOR_BGR2HSV)
            rgbMeanListHSV[i][j] = int(temp[0][0][0]), int(temp[0][0][1]), int(temp[0][0][2])

    if rgbMeanListHSV[0][2][0] >= 15:
        if rgbMeanListHSV[0][2][0] - 15 < rgbMeanListHSV[1][0][0] < rgbMeanListHSV[0][2][0] + 15:
            pass
        elif rgbMeanListHSV[0][2][0] - 15 < rgbMeanListHSV[3][0][0] < rgbMeanListHSV[0][2][0] + 15:
            imgList[1], imgList[3] = imgList[3], imgList[1]
            rgbMeanListHSV[1], rgbMeanListHSV[3] = rgbMeanListHSV[3], rgbMeanListHSV[1]
        else:
            pass
    elif rgbMeanListHSV[0][2][0] < 15:
        temp = 15 - rgbMeanListHSV[0][2][0]
        if 150-temp < rgbMeanListHSV[1][0][0] <= 150 or 0 <= rgbMeanListHSV[1][0][0] < rgbMeanListHSV[0][2][0] + 15:
            pass
        elif 150-temp < rgbMeanListHSV[3][0][0] <= 150 or 0 <= rgbMeanListHSV[3][0][0] < rgbMeanListHSV[0][2][0] + 15:
            imgList[1], imgList[3] = imgList[3], imgList[1]
            rgbMeanListHSV[1], rgbMeanListHSV[3] = rgbMeanListHSV[3], rgbMeanListHSV[1]

    rectOneHue = rgbMeanListHSV[1][1][0]
    rectTwoHue = rgbMeanListHSV[3][1][0]
    rectUpHue = rgbMeanListHSV[4][3][0]
    
    diffOfTwoAndUpperC1 = abs(rectOneHue - rectUpHue)
    if rectOneHue > rectUpHue:
        diffOfTwoAndUpperC2 = abs((180 - rectOneHue)+rectUpHue)
    else:
        diffOfTwoAndUpperC2 = abs((180 - rectUpHue) + rectOneHue)
    diffTwo = min(diffOfTwoAndUpperC1, diffOfTwoAndUpperC2)

    diffOfFourAndUpperC1 = abs(rectTwoHue - rectUpHue)
    if rectTwoHue > rectUpHue:
        diffOfFourAndUpperC2 = abs((180 - rectTwoHue) + rectUpHue)
    else:
        diffOfFourAndUpperC2 = abs((180 - rectUpHue) + rectTwoHue)
    diffFour = min(diffOfFourAndUpperC1, diffOfFourAndUpperC2)

    if diffTwo <= diffFour:
        return imageConstructor(imgList[0], imgList[1], imgList[2], imgList[3], imgList[4], imgUpLoc=2)
    elif diffFour < diffTwo:
        return imageConstructor(imgList[0], imgList[1], imgList[2], imgList[3], imgList[4], imgUpLoc=4)
    

def imageConstructor(imgLeftMost, imgLeft, imgRight, imgRightMost, imgUp, imgUpLoc):
    blackLeftMost = np.zeros_like(imgLeftMost)
    blackLeft = np.zeros_like(imgLeft)
    blackRightMost = np.zeros_like(imgRightMost)
    blackRight = np.zeros_like(imgRight)
    imgLower = np.hstack((imgLeftMost, imgLeft, imgRight, imgRightMost))
    if imgUpLoc == 1:
        imgUpper = np.hstack((imgUp, blackLeft, blackRight, blackRightMost))
    elif imgUpLoc == 2:
        imgUpper = np.hstack((blackLeftMost, imgUp, blackRight, blackRightMost))
    elif imgUpLoc == 3:
        imgUpper = np.hstack((blackLeftMost, blackLeft, imgUp, blackRightMost))
    elif imgUpLoc == 4:
        imgUpper = np.hstack((blackLeftMost, blackLeft, blackRight, imgUp))
    else:
        pass

    return np.vstack((imgUpper, imgLower))

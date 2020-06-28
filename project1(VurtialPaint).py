import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)


myColors = [[5, 22, 253, 255, 66, 255], # orange
            [75, 106, 221, 255, 66, 193], # blue
            [67, 91, 169, 255, 0, 77]] # green
myColorValues = [[51, 153, 255],      #BGR
                 [255, 255, 51],
                 [0, 204, 0]]

myPoints = []   # [x, y, colorId]


def findColor(img, myColors, myColorValues):
    img_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_Points = []
    for color in myColors:
        lower = np.array(color[0:6:2])
        upper = np.array(color[1:6:2])
        mask = cv2.inRange(img_HSV, lower, upper)
        x, y = getContours(mask)
        cv2.circle(img_Result, (x, y), 10, myColorValues[count], cv2.FILLED) # cv2.FILLED=塗りつぶし
        if x != 0 and y != 0:
            new_Points.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask)
    return new_Points

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours: # contours=輪郭リスト
        area = cv2.contourArea(cnt) # 面積

        if area > 500:
            # cv2.drawContours(img_Result, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(img_Result, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img_Result = img.copy()
    new_Points = findColor(img, myColors, myColorValues)
    if len(new_Points) != 0:
        for newP in new_Points:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow("Result", img_Result)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
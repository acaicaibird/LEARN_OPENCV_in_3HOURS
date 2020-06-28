import cv2
import numpy as np



width_Img = 640
height_Img = 480


frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10, 150)


def preProcessing(img):
    img_Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_Blur = cv2.GaussianBlur(img_Gray, (5, 5), 1)
    img_Canny = cv2.Canny(img_Blur, 200, 200)
    kernel = np.ones((5, 5))
    img_Dail = cv2.dilate(img_Canny, kernel, iterations=2)
    img_Thres = cv2.erode(img_Dail, kernel, iterations=1)

    return img_Thres

def getContours(img):
    biggest = np.array([])
    maxArea = 0
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours: # contours=輪郭リスト
        area = cv2.contourArea(cnt) # 面積
        if area >5000:
            # cv2.drawContours(img_Contour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx)  == 4:
                biggest = approx # 画面右側にあるものを優先？
                maxArea = area
    cv2.drawContours(img_Contour, biggest, -1, (255, 0, 0), 20) # 4点でdrawしている
    return biggest
            # print(len(approx))
            # objCor = len(approx)
            # x, y, w, h = cv2.boundingRect(approx)

def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1) # 列の数字を足す
    # print("add", add)

    myPointsNew[0] = myPoints[np.argmin(add)] # 0番目に代入
    myPointsNew[3] = myPoints[np.argmax(add)] # 3番目に代入
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints", myPointsNew)
    return myPointsNew

def getWarp(img, biggest):
    biggest = reorder(biggest)
    # print(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [width_Img, 0], [0, height_Img], [width_Img, height_Img]]) # 表示する画面のサイズ
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_Output = cv2.warpPerspective(img, matrix, (width_Img, height_Img))

    return img_Output



while True:
    success, img = cap.read()
    img = cv2.resize(img, (width_Img, height_Img))
    img_Contour = img.copy()

    img_Thres = preProcessing(img)
    biggest = getContours(img_Thres)
    # print(biggest) # 読み込んだ画像の輪郭の位置(x[], y[], w[], h[])
    img_Warped = getWarp(img, biggest)



    cv2.imshow("Result", img_Warped)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

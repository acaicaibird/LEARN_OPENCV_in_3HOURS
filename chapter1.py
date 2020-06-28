import cv2
import numpy as np

img = cv2.imread("images/lena.png")
kernal = np.ones((5, 5), np.uint8)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)
img_canny = cv2.Canny(img, 150, 200)
img_dialation = cv2.dilate(img_canny, kernal, iterations=1)
img_eroded = cv2.erode(img_dialation, kernal, iterations=1)

cv2.imshow("grayimage", img_gray)
cv2.imshow("blurimage", img_blur)
cv2.imshow("cannyimage", img_canny)
cv2.imshow("diakateimage", img_dialation)
cv2.imshow("eroded", img_eroded)
cv2.waitKey(0)
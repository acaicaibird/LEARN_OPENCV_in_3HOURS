import cv2 
import numpy as np

img = cv2.imread("images/lambo.png")
print(img.shape)

img_resize = cv2.resize(img, (300, 200))
print(img_resize.shape)

img_cropped = img[0:200, 200:500]


cv2.imshow("image", img)
# cv2.imshow("image_resize", img_resize)
cv2.imshow("image_cropped", img_cropped)

cv2.waitKey(0)
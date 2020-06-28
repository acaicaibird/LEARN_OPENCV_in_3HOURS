import cv2

cap = cv2.VideoCapture(0)
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.set(3, 360) # 3=width 4=height


while True:
    success, img = cap.read()
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
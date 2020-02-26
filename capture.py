#!/usr/bin/env python3

import os
import cv2

# parameter
path  = "new_path/" # "chessboard_img/"
if not os.path.exists(path):
    os.mkdir(path)

img_count    = 0
capture      = False
auto_capture = False
cnt_capture  = 0

# create mouse click
def mouse_event(event, x, y, flags, param):
    global capture
    if event == cv2.EVENT_LBUTTONDOWN:
        capture = True

cv2.namedWindow("img")
cv2.setMouseCallback("img", mouse_event)

# video capture
camera   = cv2.VideoCapture(1)
camera.set(3, 1024)
camera.set(4, 576) 
ret, img = camera.read()


while True:
    name = path + str(img_count)+".jpg"
    ret, img = camera.read()

    if auto_capture:
        if cnt_capture >= 50:  # capture per 50ms
            capture = True
            cnt_capture = 0
        else:
            cnt_capture += 1

    cv2.imshow("img", img)

    k = cv2.waitKey(1) # milliseconds
    if k == 27 or k == ord('q'):
        print('Exit with code 0')
        break

    elif k == ord('c') or k == ord('s') or capture:
        cv2.imwrite(name, img)
        print("Saved image: {}".format(name))

        img_count += 1
        capture = False

    elif k == ord('a'): # auto capture
        auto_capture = True
        print("Enable auto capture")

    elif k == ord('d'): # stop auto capture
        auto_capture = False
        cnt_capture  = 0
        print("Disable auto capture")
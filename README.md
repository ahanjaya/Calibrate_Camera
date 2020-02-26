# Calibrate Camera

This repository for calibrate camera using opencv-python

## Getting Started

These instructions will show you how to undistort images using normal checkerboard on opencv-python version


---

## Prerequisites

What things you need to run this codes:
1. python3
2. opencv (cv2) --> [Installation](https://hackmd.io/@ahanjaya/SJaGgKrNr)
3. numpy
4. glob
5. pickle 

Tested on MSI-GP63 (Leopard 8RE):

1. 8th Gen. Intel® Core™ i7 processor
2. GTX 1060 6GB GDDR5 with desktop level performance
3. Memory 16GB DDR4 2666MHz
4. SSD 256 GB
5. Ubuntu 16.04.06 LTS (with ROS Kinetic)
6. Logitech C922 webcam


---
## Table of Contents

[TOC]


---

### Checkerboard
This code tested on Checkerboard with size 8x7.

In order to re-calibrate camera, please print the checkerboard [online](https://markhedleyjones.com/projects/calibration-checkerboard-collection) or find in :
```
data/Checkerboard-A4-30mm-8x6.pdf
```

then change parameter on `calibrate.py`

```
# size chessboard
self.num_wblock  = 8
self.num_hblock  = 7
```

---

### Capturing data

```
python3 capture.py
```

This script is for generating data
1. Provide desired path to store images.
2. Press 'c' or 's' or left-mouse click to capture image.
3. Press 'q' or 'esc' to quit.
4. Mostly use 50 images for calibrate.


---

### Calibrate camera
```
python3 calibrate.py
```

for calibration:
`self.calibration = True`

for load calibration:
`self.calibration = False`

---

References
---
1. https://docs.opencv.org/master/dc/dbb/tutorial_py_calibration.html
2. https://markhedleyjones.com/projects/calibration-checkerboard-collection

---
## Appendix and FAQ

:::info
**Find this document incomplete?** Leave a comment!
:::

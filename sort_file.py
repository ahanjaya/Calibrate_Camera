#!/usr/bin/env python3

import os
import glob
import numpy as np

folder = 'chessboard_img'
images = glob.glob(folder + '/*.jpg')
order  = np.argsort([int(p.split(".")[-2].split("/")[-1]) for p in images])

images = np.array(images)
images = images[order]

new_cnt = 52
for img in images:
    os.system('cp {} {}.jpg'.format(img, new_cnt))
    new_cnt += 1
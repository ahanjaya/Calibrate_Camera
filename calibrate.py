#!/usr/bin/env python3

import cv2
import glob
import pickle
import numpy as np

class Calibration:
    def __init__(self):
        # self.camera_type = 'C922'
        self.camera_type = 'C930E'
        self.images = glob.glob('{}_image/*.jpg'.format(self.camera_type))

        # size chessboard
        self.num_wblock  = 8
        self.num_hblock  = 7

        # termination criteria
        self.criteria    = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp        = np.zeros((self.num_hblock * self.num_wblock, 3), np.float32)
        self.objp[:,:2]  = np.mgrid[0:self.num_wblock, 0:self.num_hblock].T.reshape(-1,2)

        # Arrays to store object points and image points from all the images.
        self.obj_points  = [] # 3d point in real world space
        self.img_points  = [] # 2d points in image plane.

        self.img_size     = None
        self.camera_dist  = "data/{}_dist.p".format(self.camera_type)

    def read_chessboards(self):
        for image in self.images:
            
            img  = cv2.imread(image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.img_size = gray.shape[::-1]

            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (self.num_wblock, self.num_hblock), None)

            # If found, add object points, image points (after refining them)
            if ret:
                self.obj_points.append(self.objp)
                corners2 = cv2.cornerSubPix(gray, corners, (3,3), (-1,-1), self.criteria)
                self.img_points.append(corners)
                
                # Draw and display the corners
                cv2.drawChessboardCorners(img, (self.num_wblock, self.num_hblock), corners2, ret)
                cv2.imshow('img', img)
                cv2.waitKey(100)

        cv2.destroyAllWindows()

    def calibrate_camera(self):
        print('Please wait, calibration process ... ')
        ret, self.mtx, self.dist, rvecs, tvecs = cv2.calibrateCamera(self.obj_points, self.img_points, self.img_size, None, None)
        print('Error calibration: {}'.format(ret))

        # dunp pickle
        calib_dict = {'mtx': self.mtx, 'dist': self.dist, 'img_size':self.img_size}
        print('Image size: {}'.format(self.img_size) )

        with open(self.camera_dist, "wb") as f:
            pickle.dump(calib_dict, f)
            print('Successful dump: {}'.format(self.camera_dist))

    def load_calibrate(self):
        with open(self.camera_dist, "rb") as f:
            dist_pickle = pickle.load(f)
            print('Successful load: {}'.format(self.camera_dist))

        self.mtx      = dist_pickle["mtx"]
        self.dist     = dist_pickle["dist"]
        self.img_size = dist_pickle["img_size"]
        print('Image size: {}'.format(self.img_size) )

    def undistort_test(self):
        camera   = cv2.VideoCapture("/dev/{}".format(self.camera_type))
        camera.set(3, self.img_size[0]) # 1024
        camera.set(4, self.img_size[1]) # 576
        _, img = camera.read()

        img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        h,  w    = img_gray.shape[:2]

        new_mtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))

        while True:
            _, img     = camera.read()
            undist_img =  cv2.undistort(img, self.mtx, self.dist, None, new_mtx)
            
            # crop undistorted field
            x, y, w, h = roi
            undist_img = undist_img[y:y+h, x:x+w]
            # print(undist_img.shape)

            # show frame
            cv2.imshow("original", img)
            cv2.imshow("undistorted", undist_img)

            k = cv2.waitKey(1)
            if k == 27 or k == ord('q'):
                print('Exit with code 0')
                break
        cv2.destroyAllWindows()

    def run(self):
        self.calibration = False

        if self.calibration:
            self.read_chessboards()  # 1st step
            self.calibrate_camera()  # 2nd step
        else:
            self.load_calibrate()
        
        self.undistort_test()

if __name__ == '__main__':
    calib = Calibration()
    calib.run()
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 17:53:47 2019

@author: robin
"""

import cv2
import numpy as np
cap=cv2.VideoCapture(0)
def nothing(x):
    pass
cv2.createTrackbar("Edge",'frame',0,255,nothing)
cv2.createTrackbar("Edge2",'frame',0,255,nothing)
cv2.createTrackbar("Edge3",'frame',0,255,nothing)
cv2.createTrackbar("Edge4",'frame',0,255,nothing)
while True:
    ret, frame= cap.read()
    laplacian=cv2.Laplacian(frame,cv2.CV_64F)
    sobelx=cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
    sobely=cv2.Sobel(frame,cv2.CV_64F,0,1, ksize=5)
    r=cv2.getTrackbarPos('R','frame')
    g=cv2.getTrackbarPos('G','frame')
    b=cv2.getTrackbarPos('B','frame')
    y=cv2.getTrackbarPos('Y','frame')
    edgelow=np.array([r,g])
    edgehigh=np.array([b,y])
    edges=cv2.Canny(frame,r,g)
    cv2.imshow("frame",frame)
    cv2.imshow("edges",edges)

    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
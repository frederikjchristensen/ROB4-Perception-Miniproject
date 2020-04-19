#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:47:06 2020

@author: frederik
"""

import cv2
import numpy as np

#Import image
gray = cv2.imread('IMG_20200419_125217__01.jpg', cv2.IMREAD_GRAYSCALE)
colour = cv2.imread('IMG_20200419_125217__01.jpg', cv2.IMREAD_UNCHANGED)
mask = cv2.imread('IMG_20200419_125217__01.jpg', cv2.IMREAD_UNCHANGED)


blur = cv2.medianBlur(gray,19)
th3 = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

ret,thresh = cv2.threshold(gray,127,255,0)
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(colour, contours, -1, (0,0,255), cv2.FILLED)
cv2.drawContours(mask, contours, -1, (0,0,255), cv2.FILLED)
contour_mask = cv2.inRange(mask, (0, 0, 255), (0, 0, 255))

kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))

#Apply Opening (Noise removal)
erosion = cv2.erode(contour_mask, kernel_small, 1)
dilation = cv2.dilate(erosion, kernel_large, 1)





cv2.namedWindow("Grayscale", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions   
cv2.resizeWindow("Grayscale", gray.shape[0], gray.shape[1])     
cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("Colour", gray.shape[0], gray.shape[1])    
cv2.imshow("Grayscale", gray)
cv2.imshow("Colour", colour)

cv2.namedWindow("test", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("test", gray.shape[0], gray.shape[1])  
cv2.imshow("test", dilation)






# Quit program is 'q' is pressed
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
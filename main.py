#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:47:06 2020

@author: frederik
"""

import cv2
import numpy as np

#Import image
gray = cv2.imread('IMG_20200419_114116.jpg', cv2.IMREAD_GRAYSCALE)
colour = cv2.imread('IMG_20200419_114116.jpg', cv2.IMREAD_UNCHANGED)

ret,thresh = cv2.threshold(gray,127,255,0)
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(colour, contours, -1, (0,0,255), cv2.FILLED)




cv2.namedWindow("Grayscale", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions   
cv2.resizeWindow("Grayscale", gray.shape[0], gray.shape[1])     
cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("Colour", gray.shape[0], gray.shape[1])    
cv2.imshow("Grayscale", gray)
cv2.imshow("Colour", colour)





# Quit program is 'q' is pressed
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
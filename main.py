#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:47:06 2020

@author: frederik
"""

import argparse
import imutils

import cv2, sys, os
import numpy as np
from math import copysign, log10

#Import image
gray = cv2.imread('main.jpg', cv2.IMREAD_GRAYSCALE)
colour = cv2.imread('main.jpg', cv2.IMREAD_UNCHANGED)
mask = cv2.imread('main.jpg', cv2.IMREAD_UNCHANGED)
spoon = cv2.imread('references/spoon.jpg', cv2.IMREAD_UNCHANGED)
spoongray = cv2.imread('references/spoon.jpg', cv2.IMREAD_GRAYSCALE)
meatfork = cv2.imread('references/meatfork.jpg', cv2.IMREAD_GRAYSCALE)
scissor = cv2.imread('references/scissor.jpg', cv2.IMREAD_GRAYSCALE)
spatula = cv2.imread('references/spatula.jpg', cv2.IMREAD_GRAYSCALE)
whisker = cv2.imread('references/whisker.jpg', cv2.IMREAD_GRAYSCALE)


huMomentsRef = [0]*7   #Holder for reference values
huMomentsContour = [0]*7 #Holder for current contour values

def spoonspotter():
    ret,thresh = cv2.threshold(spoongray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(spoon, contours, -1, (0,0,255), cv2.FILLED)
    contour_mask = cv2.inRange(spoon, (0, 0, 255), (0, 0, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6)) 
    #Apply Opening (Noise removal)
    opening = cv2.morphologyEx(contour_mask, cv2.MORPH_OPEN, kernel_small)
    
    # Calculate Moments
    moments = cv2.moments(contour_mask)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Log scale hu moments
    for i in range(0,7):
        huMomentsRef[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))

    
    cv2.namedWindow("Spoon", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
    cv2.resizeWindow("Spoon", spoon.shape[0], spoon.shape[1])  
    cv2.imshow("Spoon", spoon)
        


blur = cv2.GaussianBlur(gray,(5,5),0)

ret,thresh = cv2.threshold(blur,100,100,0)
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(colour, contours, -1, (0,0,255), cv2.FILLED)
cv2.drawContours(mask, contours, -1, (0,0,255), cv2.FILLED)
contour_mask = cv2.inRange(mask, (0, 0, 255), (0, 0, 255))


kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

#Apply Opening (Noise removal)
opening = cv2.morphologyEx(contour_mask, cv2.MORPH_OPEN, kernel_small)
dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)

# Calculate Moments
moments = cv2.moments(contour_mask)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)


# For center stuff
cnts = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
no_contours = cnts.__len__()
cnts = imutils.grab_contours(cnts)

for x in cnts:
    # compute the center of the contour
    M = cv2.moments(x)
    #Solves division by zero errors. 
    if (M["m00"] == 0):
        M["m00"] = 1
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    # draw the contour and center of the shape on the image
    cv2.drawContours(colour, [x], -1, (0, 255, 0), 2)
    cv2.circle(colour, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(colour, "center", (cX - 20, cY - 20),
	cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


spoonspotter()
cv2.namedWindow("Grayscale", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions   
cv2.resizeWindow("Grayscale", gray.shape[0], gray.shape[1])     
cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("Colour", gray.shape[0], gray.shape[1])    
cv2.imshow("Grayscale", gray)
cv2.imshow("Colour", colour)

cv2.namedWindow("test", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("test", gray.shape[0], gray.shape[1])  
cv2.imshow("test", erosion)






# Quit program is 'q' is pressed
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
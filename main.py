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
meatfork = cv2.imread('references/meatfork.jpg', cv2.IMREAD_UNCHANGED)
meatforkgray = cv2.imread('references/meatfork.jpg', cv2.IMREAD_GRAYSCALE)
scissor = cv2.imread('references/scissor.jpg', cv2.IMREAD_UNCHANGED)
scissorgray = cv2.imread('references/scissor.jpg', cv2.IMREAD_GRAYSCALE)
spatula = cv2.imread('references/spatula.jpg', cv2.IMREAD_UNCHANGED)
spatulagray = cv2.imread('references/spatula.jpg', cv2.IMREAD_GRAYSCALE)
whisker = cv2.imread('references/whisker.jpg', cv2.IMREAD_UNCHANGED)
whiskergray = cv2.imread('references/whisker.jpg', cv2.IMREAD_GRAYSCALE)


huMomentsRef = [0]*7   #Holder for reference values
#huMomentsContour = [0]*7 #Holder for current contour values

def spoonspotter():
    ret,thresh = cv2.threshold(spoongray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(spoon, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_spoon
    contour_mask_spoon = cv2.inRange(spoon, (255, 255, 255), (255, 255, 255))
    
    #kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6)) 
    #Apply Opening (Noise removal)
    #opening = cv2.morphologyEx(contour_mask, cv2.MORPH_OPEN, kernel_small)
    
    
    # Calculate Moments
    moments = cv2.moments(contour_mask_spoon)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Log scale hu moments
    #print("SPOON")
    for i in range(0,7):
        huMomentsRef[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
      #  print(huMomentsRef[i])
    
    cv2.namedWindow("Spoon", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
    cv2.resizeWindow("Spoon", spoon.shape[0], spoon.shape[1])  
    cv2.imshow("Spoon", spoon)

def spatulaspotter():
    ret,thresh = cv2.threshold(spatulagray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(spatula, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_spatula
    contour_mask_spatula = cv2.inRange(spatula, (255, 255, 255), (255, 255, 255))
    
    #kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6)) 
    #Apply Opening (Noise removal)
    #opening = cv2.morphologyEx(contour_mask, cv2.MORPH_OPEN, kernel_small)
    
    
    # Calculate Moments
    moments = cv2.moments(contour_mask_spatula)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Log scale hu moments
    #print("SPOON")
    for i in range(0,7):
        huMomentsRef[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
      #  print(huMomentsRef[i])
    
    cv2.namedWindow("Spatula", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
    cv2.resizeWindow("Spatula", spatula.shape[0], spatula.shape[1])  
    cv2.imshow("Spatula", spatula)


def whiskerspotter():
    ret,thresh = cv2.threshold(whiskergray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(whisker, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_whisker
    contour_mask_whisker = cv2.inRange(whisker, (255, 255, 255), (255, 255, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

    #Apply Opening (Noise removal)
    opening = cv2.morphologyEx(contour_mask_whisker, cv2.MORPH_OPEN, kernel_small)
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
    erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)
    contour_mask_whisker = erosion
    
    # Calculate Moments
    moments = cv2.moments(contour_mask_whisker)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Log scale hu moments
    #print("SPOON")
    for i in range(0,7):
        huMomentsRef[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
      #  print(huMomentsRef[i])
    
    cv2.namedWindow("Whisker", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
    cv2.resizeWindow("Whisker", whisker.shape[0], whisker.shape[1])  
    cv2.imshow("Whisker", whisker)

def meatforkspotter():
    ret,thresh = cv2.threshold(meatforkgray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(meatfork, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_meatfork
    contour_mask_meatfork = cv2.inRange(meatfork, (255, 255, 255), (255, 255, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

    #Apply Opening (Noise removal)
    opening = cv2.morphologyEx(contour_mask_meatfork, cv2.MORPH_OPEN, kernel_small)
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
    erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)
    contour_mask_meatfork = erosion
    
    # Calculate Moments
    moments = cv2.moments(contour_mask_meatfork)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Log scale hu moments
    #print("SPOON")
    for i in range(0,7):
        huMomentsRef[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
      #  print(huMomentsRef[i])
    
    
def scissorspotter():
    ret,thresh = cv2.threshold(scissorgray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(scissor, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_scissor
    contour_mask_scissor = cv2.inRange(scissor, (255, 255, 255), (255, 255, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

    #Apply Opening (Noise removal)
    opening = cv2.morphologyEx(contour_mask_scissor, cv2.MORPH_OPEN, kernel_small)
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
    erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)
    contour_mask_scissor = erosion
    
    # Calculate Moments
    moments = cv2.moments(contour_mask_scissor)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    # Log scale hu moments
    #print("SPOON")
    for i in range(0,7):
        huMomentsRef[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
      #  print(huMomentsRef[i])

    cv2.namedWindow("Scissor", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
    cv2.resizeWindow("Scissor", scissor.shape[0], scissor.shape[1])  
    cv2.imshow("Scissor", scissor)


# MAIN CODE ###########################


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
    #huMoments = cv2.HuMoments(M)
    #print("HuMomentsContour")
    # Log scale hu moments
    #for i in range(0,7):
     #   huMoments[i] = -1* copysign(1.0, huMoments[i]) * log10(abs(huMoments[i]))
      #  print(huMoments[i])
    
    #Spoon shape matcher
    spoonspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d1 = cv2.matchShapes(compare,contour_mask_spoon,cv2.CONTOURS_MATCH_I2,0)
    #print("D1 %s", d1)
    if (d1 < 0.02):
        cv2.drawContours(colour, [x], -1, (255, 25, 25), 2)
        cv2.putText(colour, "Spoon", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    #Spatula shape matching    
    spatulaspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d2 = cv2.matchShapes(compare,contour_mask_spatula,cv2.CONTOURS_MATCH_I2,0)
    #print("D2 %s", d2)
    if (d2 < 0.02):
        cv2.drawContours(colour, [x], -1, (25, 25, 255), 2)
        cv2.putText(colour, "Spatula", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
    #Whisker shape matching    
    whiskerspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d3 = cv2.matchShapes(compare,contour_mask_whisker,cv2.CONTOURS_MATCH_I2,0)
    if (d3 < 0.02):
        cv2.drawContours(colour, [x], -1, (25, 255, 255), 2)
        cv2.putText(colour, "Whisker", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        print("D3 %s", d3)
        
    #Meatfork shape matching    
    meatforkspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d4 = cv2.matchShapes(compare,contour_mask_meatfork,cv2.CONTOURS_MATCH_I2,0)
    #print("D4 %s", d4)
    if (d4 < 0.1): #Shape vastly different from others, so higher pass value allowed.
        cv2.drawContours(colour, [x], -1, (25, 255, 255), 2)
        cv2.putText(colour, "Meatfork", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        
    #Scissor shape matching    
    scissorspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d5 = cv2.matchShapes(compare,contour_mask_scissor,cv2.CONTOURS_MATCH_I2,0)
    if (d5 < 0.01): #Shape is very generic, so a strict limit is set.
        cv2.drawContours(colour, [x], -1, (25, 255, 255), 2)
        cv2.putText(colour, "Scissor", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
        print("D5 %s", d5)

    
    # draw the contour and center of the shape on the image
    #cv2.drawContours(colour, [x], -1, (0, 255, 0), 2)
    cv2.circle(colour, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(colour, "center", (cX - 20, cY - 20),
	cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


cv2.namedWindow("Grayscale", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions   
cv2.resizeWindow("Grayscale", gray.shape[0], gray.shape[1])     
cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("Colour", gray.shape[0], gray.shape[1])    
cv2.imshow("Grayscale", gray)
cv2.imshow("Colour", colour)

cv2.namedWindow("test", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("test", gray.shape[0], gray.shape[1])  
cv2.imshow("test", contour_mask_spoon)

cv2.namedWindow("test2", cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions    
cv2.resizeWindow("test2", gray.shape[0], gray.shape[1])  
cv2.imshow("test2", compare)






# Quit program is 'q' is pressed
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
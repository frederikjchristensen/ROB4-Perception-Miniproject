#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:47:06 2020

@author: frederik
"""
"""
Any lines of codes that has been commented out, are for testing.

"""

#import argparse     (From attempt to use huMoments as feature)
import imutils

import cv2#, sys, os (From attempt to use huMoments as feature)
#import numpy as np (From attempt to use huMoments as feature)
#from math import copysign, log10 (From attempt to use huMoments as feature)

#Import image
gray = cv2.imread('main.jpg', cv2.IMREAD_GRAYSCALE) #Both Greyscale and colour versions are used in image proccesing.
# Grayscales for contour finding, and the colours with filled contours drawn over, to extract silhouettes.
colour = cv2.imread('main.jpg', cv2.IMREAD_UNCHANGED)
mask = cv2.imread('main.jpg', cv2.IMREAD_UNCHANGED)

# All of the below images, are extracting a silhouette and using it for shape matching
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
# All of these images are references, kind of like a database of what we are looking for.
# They are all turned into binary silhouette images, which will be compared to silhouettes in the recorded image.



#huMomentsRef = [0]*7   #Holder for reference values
#huMomentsContour = [0]*7 #Holder for current contour values


# Every spotter function simply, takes the reference, of an object we know what is, extracts a silhouette, and compares it silhouettes
# In the main image.
def spoonspotter():
    ret,thresh = cv2.threshold(spoongray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #The RETR_TREE and CHAIN_APPROX_SIMPLE was
    #Chosen after much testing which was the best method and got the best results.
    
    cv2.drawContours(spoon, contours, -1, (255,255,255), cv2.FILLED) #Draws the all (-1) contours filled white.
    global contour_mask_spoon #It is neccesary for the code to function to globally define the image.
    contour_mask_spoon = cv2.inRange(spoon, (255, 255, 255), (255, 255, 255)) # Makes a binary image (silhouette) from the coloured image
    # In hinsight i actually didn't need colour references.
    

def spatulaspotter():
    ret,thresh = cv2.threshold(spatulagray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(spatula, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_spatula
    contour_mask_spatula = cv2.inRange(spatula, (255, 255, 255), (255, 255, 255))



def whiskerspotter():
    ret,thresh = cv2.threshold(whiskergray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(whisker, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_whisker
    contour_mask_whisker = cv2.inRange(whisker, (255, 255, 255), (255, 255, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

    #Apply Opening (Noise removal) The purpose was to reduce the number of contours spottet in the whisker wires. 
    opening = cv2.morphologyEx(contour_mask_whisker, cv2.MORPH_OPEN, kernel_small)
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
    erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)
    contour_mask_whisker = erosion
    

def meatforkspotter():
    ret,thresh = cv2.threshold(meatforkgray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(meatfork, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_meatfork
    contour_mask_meatfork = cv2.inRange(meatfork, (255, 255, 255), (255, 255, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

    #Apply Opening (Noise removal) There was alot of contours around the handle, and this reduces it.
    opening = cv2.morphologyEx(contour_mask_meatfork, cv2.MORPH_OPEN, kernel_small)
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
    erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)
    contour_mask_meatfork = erosion
    
    
    
def scissorspotter():
    ret,thresh = cv2.threshold(scissorgray,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    cv2.drawContours(scissor, contours, -1, (255,255,255), cv2.FILLED)
    global contour_mask_scissor
    contour_mask_scissor = cv2.inRange(scissor, (255, 255, 255), (255, 255, 255))
    
    kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
    kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

    #Apply Opening (Noise removal) The blade due to it's shine, had alot of contours, also every blade was it's own contour.
    # Again using morphology, it was reduced and brought together.
    opening = cv2.morphologyEx(contour_mask_scissor, cv2.MORPH_OPEN, kernel_small)
    dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
    erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)
    contour_mask_scissor = erosion
    




# MAIN CODE ###########################
blur = cv2.GaussianBlur(gray,(5,5),0) 
# Due to imperfections in the background, and small noise, a slight blur was applied to drown noise.

ret,thresh = cv2.threshold(blur,100,100,0)
contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(colour, contours, -1, (0,0,255), cv2.FILLED)
cv2.drawContours(mask, contours, -1, (0,0,255), cv2.FILLED)
contour_mask = cv2.inRange(mask, (0, 0, 255), (0, 0, 255))

# The image is 4k resolution, in the future the kernel sizes would need to be a function depending on the image resolution.
kernel_small = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6, 6))
kernel_large = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (39, 39))

#Apply Opening (Noise removal)
opening = cv2.morphologyEx(contour_mask, cv2.MORPH_OPEN, kernel_small)
dilation = cv2.morphologyEx(opening, cv2.MORPH_DILATE, kernel_large)
erosion = cv2.morphologyEx(dilation, cv2.MORPH_ERODE, kernel_large)

# For center stuff, bassicly location the center of the contour in order to just write the identified class properly near the contour.
cnts = cv2.findContours(erosion.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
no_contours = cnts.__len__()
cnts = imutils.grab_contours(cnts) #This saves all the contours and makes them available to go through one by one in a for loop.

for x in cnts:
    # compute the center of the contour
    M = cv2.moments(x)
    #Solves division by zero errors. 
    if (M["m00"] == 0):
        M["m00"] = 1 #Sometimes contours will experience and error, and since you can't divide by zero, this fixes any runtime errors.
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
    compare = colour.copy() # Copies a version of the main images coloured to use as comparison
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED) #Draws the current contour in the for loop.
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255)) # Creates a Binary silhouette image from main image using "x" contour.
    d1 = cv2.matchShapes(compare,contour_mask_spoon,cv2.CONTOURS_MATCH_I2,0) # Runs matchshapes function, and gets a value describing "deviation"
    # The lower the number the better the match, usually around 0.1 or lower.

    
    #Spatula shape matching    
    spatulaspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d2 = cv2.matchShapes(compare,contour_mask_spatula,cv2.CONTOURS_MATCH_I2,0)

        
    #Whisker shape matching    
    whiskerspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d3 = cv2.matchShapes(compare,contour_mask_whisker,cv2.CONTOURS_MATCH_I2,0)
    # The scissor is for some reason identified as a whisker, despite their silhouettes being so different.
    # Still haven't figured out why the shape matching is dead accurate on the scissor.

        
    #Meatfork shape matching    
    meatforkspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d4 = cv2.matchShapes(compare,contour_mask_meatfork,cv2.CONTOURS_MATCH_I2,0)

        
    #Scissor shape matching    
    scissorspotter()
    compare = colour.copy()
    cv2.drawContours(compare, [x], -1, (0, 205, 255), cv2.FILLED)
    compare = cv2.inRange(compare, (0, 205, 255), (0, 205, 255))
    d5 = cv2.matchShapes(compare,contour_mask_scissor,cv2.CONTOURS_MATCH_I2,0)

    
    # The values for the diviations was chosen based off how closely a silhouette is allowed to diviate from the reference "ideal" silhouette.
    # It works very well with a low number like 0.15, it is low enough that a spoon and whisker, whish have very similar silhouettes aren't mixed.
    # However, for some reason the scissor is recognized as a whisker, despite having nowhere near similar silhouette, yet it gets very low diviation values.
    # The root of the issue, is still unknown.
    #Sorting classification
    if (d1 < 0.15 and d1 < d2 and d1 < d3 and d1 < d4 and d1 < d5): #If criteria, low diviation of d1, the spoon criteria, and 
        # D1 still has to the be lowest of all other diviations, bassicly, in english, it  diviates the least from being a spoon.
        cv2.drawContours(colour, [x], -1, (255, 25, 25), 2) #Draw the identified contour, this time only an edge with pixel width 2.
        # In a seperate colour from other classes.
        cv2.putText(colour, "Spoon", (cX + 40, cY + 20), # Draws the name of the utensil slightly offset from the center of the contour.
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    if (d2 < 0.15 and d2 < d1 and d2 < d3 and d2 < d4 and d2 < d5):
        cv2.drawContours(colour, [x], -1, (25, 25, 255), 2)
        cv2.putText(colour, "Spatula", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    if (d3 < 0.15 and d3 < d1 and d3 < d2 and d3 < d4 and d3 < d5):
        cv2.drawContours(colour, [x], -1, (25, 255, 255), 2)
        cv2.putText(colour, "Whisker", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    if (d4 < 0.15 and d4 < d1 and d4 < d2 and d4 < d3 and d4 < d5): 
        cv2.drawContours(colour, [x], -1, (25, 255, 255), 2)
        cv2.putText(colour, "Meatfork", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    if (d5 < 0.15 and d5 < d1 and d5 < d2 and d5 < d3 and d5 < d4): 
        cv2.drawContours(colour, [x], -1, (25, 255, 255), 2)
        cv2.putText(colour, "Scissor", (cX + 40, cY + 20),
        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2)
    
    
    # draw the contour and center of the shape on the image
    #cv2.drawContours(colour, [x], -1, (0, 255, 0), 2)
    cv2.circle(colour, (cX, cY), 7, (255, 255, 255), -1) #Draws small circle around center.
    cv2.putText(colour, "center", (cX - 20, cY - 20), #Draws "center" around center
	cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

  
cv2.namedWindow("Colour", cv2.WINDOW_NORMAL)   # Create window with free diemnsions
cv2.resizeWindow("Colour", gray.shape[0], gray.shape[1]) #Resizes the window to fit the image displayed.
cv2.imshow("Colour", colour) #Shows image.






# Quit program is 'q' is pressed
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
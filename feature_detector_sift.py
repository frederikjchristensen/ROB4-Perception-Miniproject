#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:56:56 2020

@author: frederik
"""

import cv2
import numpy as np

img = cv2.imread("references/spatula.jpg", cv2.IMREAD_GRAYSCALE)

sift = cv2.xfeatures2d.SIFT_create()

kp = sift.detect(img, None)

img = cv2.drawKeypoints(img, kp, None)

cv2.imshow("image", img)
# Quit program is 'q' is pressed
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
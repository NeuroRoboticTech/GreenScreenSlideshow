#!/usr/bin/env python
#
# Green screen slidesow.
# v1.0.0
#
# This class scans two folders looking for video or images. The first is 
# a folder with green screen pictures and the second is one with background
# images or video. It then randomly picks picturs/video from each and displays
# them for a time.
#
'''
## License

  COPYRIGHT (C) 2016 NeuroRobotic Technologies, LLC
  ALL RIGHTS RESERVED. This code is not for public use.

'''

# David Cofer
# Initial Date: 10 June 2016
# Last Updated: 10 June 2016
# http://www.NeuroRoboticTech.com/

import os
import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
import copy
import random
from datetime import datetime

def findFiles(input_dir, file_typea): 
    #Get the files in the directory of the given type
    files_list = [fn for fn in os.listdir(input_dir)
                    if any(fn.endswith(ext) for ext in file_typea)]
    files = sorted(set(files_list))
    return files

scale_factor = 1.0
random.seed(datetime.now())
    
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--greenscreen_images", required = False, help = "Path to the source green screen image")
ap.add_argument("-b", "--background_images", required = False, help = "Path to background images")
args = vars(ap.parse_args())

if args["greenscreen_images"] is None:
    args["greenscreen_images"] = "C:\\Projects\GreenScreenSlideShow\GreenScreens"
if args["background_images"] is None:
    args["background_images"] = "C:\\Projects\GreenScreenSlideShow\Backgrounds"

print "Starting up"
    
# Read in images
greenScreenPath = args["greenscreen_images"]
print("GreenScreen path: %s" % greenScreenPath)

backgroundPath = args["background_images"]
print("Background path: %s" % backgroundPath)

c = ''
background_images = findFiles(backgroundPath, ['.JPG', '.jpg', '.png', '.PNG'])
greenscreen_images = findFiles(greenScreenPath, ['.JPG', '.jpg', '.png', '.PNG'])
#print "Background image list:"
#print background_images

#print "Greenscreen image list:"
#print greenscreen_images

while c != 113:

	if len(background_images) > 1:
		selBackground = random.randrange(0, len(background_images)-1)
	else:
		selBackground = 0
		
	if len(greenscreen_images) > 1:
		selGreenScreen = random.randrange(0, len(greenscreen_images)-1)
	else:
		selGreenScreen = 0

	background_file = backgroundPath + "\\" + background_images[selBackground]
	print "Background File: " + background_file
	background = cv2.imread(background_file)
	#cv2.imshow("background" ,background)

	greenscreen_file = greenScreenPath + "\\" + greenscreen_images[selGreenScreen]
	print "GreenScreen File: " + greenscreen_file
	greenscreen = cv2.imread(greenscreen_file)
	#cv2.imshow("greenscreen" ,greenscreen)

	#green_rows, green_cols, green_depth = greenscreen.shape
	#print "green_cols: ", green_cols
	#print "green_rows: ", green_rows
	
	#if green_cols > green_rows:
	#	rotM = cv2.getRotationMatrix2D((green_cols/2,green_rows/2),90,1)
	#	greenscreen = cv2.warpAffine(greenscreen,rotM,(green_cols,green_rows))
	
	#Now create a mask for the green portion of the greenscreen
	lower_green = np.array([30, 50, 0])
	upper_green = np.array([80, 255, 255])

	hsv = cv2.cvtColor(greenscreen, cv2.COLOR_BGR2HSV)

	#print hsv[0,0]

	# Threshold the HSV image to get only bright green colors
	init_mask = cv2.inRange(hsv, lower_green, upper_green)
	inv_mask =  cv2.bitwise_not(init_mask)

	#kernel = np.ones((15,15),np.float32)/225
	#smoothed = cv2.filter2D(inv_mask,-1,kernel)

	#kernel = np.ones((3, 3), np.uint8)
	#eroded_mask = cv2.erode(init_mask, kernel, iterations = 2)
	#dilated_mask = cv2.dilate(smoothed, kernel, iterations = 1)
	#dilated_mask = eroded_mask

	cut_img = cv2.bitwise_and(greenscreen, greenscreen, mask = inv_mask)
	print cut_img.shape
	print background.shape

	scale_img = cv2.resize(cut_img, (int(background.shape[1]/scale_factor), int(background.shape[0]/scale_factor)), 0, 0, interpolation = cv2.INTER_AREA)
	print scale_img.shape

	add_img = np.zeros([background.shape[0], background.shape[1], background.shape[2]])
	print add_img.shape

	add_img[(background.shape[0]- int(background.shape[0]/scale_factor)):background.shape[0], 0:int(background.shape[1]/scale_factor), :] = scale_img/255.0

	scale_init_mask = cv2.resize(init_mask, (int(background.shape[1]/scale_factor), int(background.shape[0]/scale_factor)), 0, 0, interpolation = cv2.INTER_AREA)
	back_cut_img = cv2.bitwise_and(background, background, mask = scale_init_mask)

	comb_img = back_cut_img/255.0 + add_img

	cv2.namedWindow("cut img", cv2.WND_PROP_FULLSCREEN)          
	cv2.setWindowProperty("cut img", cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
	cv2.imshow("cut img", comb_img)
	#Wait 10 seconds and then go to next image
	c = cv2.waitKey(5000)  
	print c
		
print "shutting down"

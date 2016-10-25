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

import argparse
import cv2
import numpy as np
from matplotlib import pyplot as plt
import image_utils
import copy
import random
from datetime import datetime

def findFiles(input_dir, file_type): 
    #Get the files in the directory of the given type
    included_extenstions = [file_type]
    files_list = [fn for fn in os.listdir(input_dir)
                    if any(fn.endswith(ext) for ext in included_extenstions)]
    files = sorted(set(files_list))
    return files


random.seed(datetime.now())
    
ap = argparse.ArgumentParser()
ap.add_argument("-g", "--greenscreen_images", required = False, help = "Path to the source green screen image")
ap.add_argument("-b", "--background_images", required = False, help = "Path to background images")
args = vars(ap.parse_args())

if args["greenscreen_images"] is None:
    args["greenscreen_images"] = "./GreenScreens"
if args["background_images"] is None:
    args["background_images"] = "./Backgrounds"
    
# Read in images
greenScreenPath = args["greenscreen_images"]
print("GreenScreen path: %s" % greenScreenPath)

backgroundPath = args["background_images"]
print("Background path: %s" % backgroundPath)

c = ''
#while c != 'q' && c!= 'Q':
background_images = findFiles(backgroundPath, '.JPG')
greenscreen_images = findFiles(greenScreenPath, '.JPG')

selBackground = random.randrange(0, len(background_images)-1)
selGreenScreen = random.randrange(0, len(greenscreen_images)-1)

background = cv2.imread(background_images[selBackground])
greenscreen = cv2.imread(greenscreen_images[selGreenScreen])

#Now create a mask for the green portion of the greenscreen
lower_green = np.array([median_green-60,50,50])
upper_green = np.array([median_green+60,255,255])

# Threshold the HSV image to get only bright green colors
mask = cv2.inRange(greenscreen, lower_green, upper_green)

cv2.imshow("mask" ,mask)
cv2.waitKey(0)  

    


__author__ = 'Ben'
#test script for picamera
import picamera
import time
import picamera.array
import io
import RPi.GPIO as GPIO
import numpy as np
from neopixel import *
from fractions import Fraction
import cv2
#from PIL import Image
import pickle
import timeit





imageorig = pickle.load(open( "frame.p", "rb" ))



THRESHOLD = 50

leds = [None]*320


def edwin(image):
    for i in range(320):
        # row col color
        if image[i][30][1] > THRESHOLD:
            leds[i] = Color(0,0,255)
        else:
            leds[i] = Color(0,0,0)


def ben(image):
    # this assumes that the image is 320 by 60

    count = 320*60*3

    image2 = np.reshape(image, count).tolist()

    # starting from 30'th pixel, moving foward 60 pixels at a time (to arrive on the pixel "below" it)
    imageslice = image2[30*3:count:60*3]

    con = Color(0,0,255)
    coff = Color(0,0,0)


    print type(imageslice)
    print type(imageslice[0])

    imageslice = bytearray(imageslice)

    print type(imageslice)
    print type(imageslice[0])


    for i in range(320):
        if imageslice[i] > THRESHOLD:
            # ledson += 1
           print "p %d on" % i
            # strip.setPixelColor(320-i, con)
        else:
            print "p %d off" % i
            # strip.setPixelColor(320-i, coff)

    #bits = [con if p > THRESHOLD else coff for p in strip]

    #print bits


    # selecting column thirty
    # print image2[30*3:1000:60*3]



# print timeit.timeit('edwin(imageorig)', "from __main__ import edwin, imageorig", number=100)
# print timeit.timeit('ben(imageorig)', "from __main__ import ben, imageorig", number=100)

# edwin(imageorig)
# print leds
ben(imageorig)






# print image
import zmq
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
import threading



zmq_context = zmq.Context()
zsock = zmq_context.socket(zmq.SUB)
zsock.setsockopt(zmq.SUBSCRIBE, '') # empty string here subscribes to all channels
port = 6000
zsock.connect('tcp://127.0.0.1:%d' % port)

poller = zmq.Poller()
poller.register(zsock, zmq.POLLIN)


# LED strip configuration:
LED_COUNT      = 320    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LOOP = 200

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()
con = Color(0,0,5)
coff = Color(0,0,0)


prevleds = [0] * LED_COUNT

# set all off
for i in range(LED_COUNT):
    strip.setPixelColor(i, coff)
strip.show()


print 'hello from led writer'

j = 0
starttime = time.time()
while(1):
    socks = dict(poller.poll(0))


    if zsock in socks and socks[zsock] == zmq.POLLIN:
        currentleds = zsock.recv_pyobj()

        for i in range(LED_COUNT):
            if currentleds[i] > prevleds[i]:
                strip.setPixelColor(LED_COUNT-i, con)
            elif currentleds[i] < prevleds[i]:
                strip.setPixelColor(LED_COUNT-i, coff)

        prevleds = list(currentleds)

        strip.show()

        j+=1

        if( j % LOOP == (LOOP-1) ):
            print('LED Average: %.2f FPS' % (LOOP/(time.time()-starttime)))
            starttime = time.time()


            # strip.setPixelColor(i, con)
            # strip.show()




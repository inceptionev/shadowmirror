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
import zmq
import threading


def threshold_main():

    print 'threshold_main starting'
    zmq_context = zmq.Context.instance()
    zsock = zmq_context.socket(zmq.SUB)
    zsock.setsockopt(zmq.SUBSCRIBE, '') # empty string here subscribes to all channels
    zsock.bind('inproc://threshold')
    poller = zmq.Poller()
    poller.register(zsock, zmq.POLLIN)

    j = 0
    while True:
        socks = dict(poller.poll(0))
        if zsock in socks and socks[zsock] == zmq.POLLIN:
            j+=1
            image = zsock.recv_pyobj()

            count = 320*60*3

            image2 = np.reshape(image, count).tolist()

            # starting from 30'th pixel, moving foward 60 pixels at a time (to arrive on the pixel "below" it)
            imageslice = image2[30*3:count:60*3]

            con = Color(0,0,255)
            coff = Color(0,0,0)

            # ledson = 0

            for i in range(strip.numPixels()):
                if imageslice[i] > THRESHOLD:
                    # ledson += 1
                    strip.setPixelColor(320-i, con)
                else:
                    strip.setPixelColor(320-i, coff)

            # for p in strip:
            #     if p > THRESHOLD:
            # bits = [Color(0,0,255) if p > THRESHOLD else Color(0,0,0) for p in strip]
            strip.show()

            # print "updated strip with %d leds lit" % ledson

            if( j == LOOP):
                print('Average: %.2f FPS' % (LOOP/(time.time()-starttime)))



def transfer():
    zmq_context = zmq.Context.instance()
    zsock = zmq_context.socket(zmq.PUB)
    zsock.connect('inproc://threshold')

    stream = picamera.array.PiRGBArray(camera)
    #stream=io.BytesIO()
    while True:
        yield stream
        stream.seek(0)
        #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        #image = cv2.imdecode(data,1)
        #image = Image.open(stream)
        image=stream.array
        zsock.send_pyobj(image)

        #pickle.dump(image, open( "frame.p", "wb" ))
        #print 'done'
        #while(1):
        #    pass

        stream.seek(0)
        stream.truncate()
        
# LED strip configuration:
LED_COUNT      = 320    # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

#settings
THRESHOLD = 190
LOOP = 2000
# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

#create and configure camera
camera=picamera.PiCamera(sensor_mode=7)
camera.resolution=(60,320)
camera.framerate=90
camera.iso = 400
#camera.shutter_speed = 12000
camera.start_preview(fullscreen=False,window=(120,1,320,240))
camera.led=False
print 'sleeping for camera'
time.sleep(2)
#lock in values
g = camera.awb_gains
camera.exposure_mode = 'off'
camera.awb_mode = 'off'
camera.awb_gains = g

# launch first thread
threshold_thread = threading.Thread(target=threshold_main)
threshold_thread.start()
print 'sleeping for threads'
time.sleep(1) # sleep so threads can run first

starttime = time.time()
camera.capture_sequence(transfer(), 'rgb', use_video_port=True)
#print('Captured %dx%d image' % (stream.array.shape[1], stream.array.shape[0]))
print('Average: %.2f FPS' % (LOOP/(time.time()-starttime)))    

camera.stop_preview()
camera.close()

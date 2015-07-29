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


def print_hex(str):
    print 'hex:'
    for b in str:
        print ' ', format(ord(b), '02x')



def threshold_main():
    starttime = time.time()
    print 'threshold_main starting'
    zmq_context = zmq.Context.instance()

    # zmq camera->threshold
    zsock = zmq_context.socket(zmq.SUB)
    zsock.setsockopt(zmq.SUBSCRIBE, '') # empty string here subscribes to all channels
    zsock.bind('inproc://threshold')
    poller = zmq.Poller()
    poller.register(zsock, zmq.POLLIN)

    # zmq threshold -> show
    # zsock2 = zmq_context.socket(zmq.PUB)
    # zsock2.connect('inproc://show')
    zsock2 = zmq_context.socket(zmq.PUB)
    zsock2.bind('tcp://*:%d' % 6000)


    con = Color(0,0,5)
    coff = Color(0,0,0)

    prevleds = [0] * LED_COUNT

    # set all off
    # for i in range(LED_COUNT):
    #     strip.setPixelColor(i, coff)
    # strip.show()

    j = 0
    while True:
        socks = dict(poller.poll(0))
        if zsock in socks and socks[zsock] == zmq.POLLIN:
            j+=1
            imageslice = zsock.recv()

            count = LED_COUNT*60*3

            currentleds = [0] * LED_COUNT

            for i in range(LED_COUNT):
                if ord(imageslice[i]) > THRESHOLD:
                    currentleds[i] = 1

            # this is the same as strip.show()
            zsock2.send_pyobj(currentleds)

            if( j % LOOP == (LOOP-1) ):
                print('Camera Average: %.2f FPS' % (LOOP/(time.time()-starttime)))
                starttime = time.time()


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

        count = 320*60*3
        image2 = np.reshape(image, count).tolist()
        imageslice = image2[30*3:count:60*3]

        # print "----"
        # print imageslice
        # bytes = bytearray(imageslice)
        # print_hex(bytes)
        # print "\n\n"


        # print type(imageslice)
        zsock.send(bytearray(imageslice))
        # zsock.send_pyobj(imageslice)

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
LOOP = 200
# Create NeoPixel object with appropriate configuration.
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
# strip.begin()

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
# threshold_thread = threading.Thread(target=show_main)
# threshold_thread.start()
print 'sleeping for threads'
time.sleep(0.1) # sleep so threads can run first

# starttime = time.time()
camera.capture_sequence(transfer(), 'rgb', use_video_port=True)
#print('Captured %dx%d image' % (stream.array.shape[1], stream.array.shape[0]))
# print('Average: %.2f FPS' % (LOOP/(time.time()-starttime)))

camera.stop_preview()
camera.close()

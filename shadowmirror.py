#test script for picamera
import picamera
import time
import picamera.array
import io
import RPi.GPIO as GPIO
import numpy as np
from neopixel import *

# LED strip configuration:
LED_COUNT      = 72      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

#create and configure camera
camera=picamera.PiCamera(sensor_mode=7)
camera.resolution=(640,480)
camera.framerate=80
camera.iso = 400
camera.start_preview(fullscreen=False,window=(120,1,640,480))
camera.led=False
time.sleep(2)
#lock in values
camera.shutter_speed = camera.exposure_speed
camera.exposure_mode = 'off'
g = camera.awb_gains
camera.awb_mode = 'off'
camera.awb_gains = g


stream=picamera.array.PiRGBArray(camera)
for x in range(0,200):
    camera.capture(stream, 'rgb', use_video_port=True)
    #print('Captured %dx%d image' % (stream.array.shape[1], stream.array.shape[0]))
    image=stream.array
    print(image[1][1])
    stream.seek(0)
    for i in range(strip.numPixels()):
        if image[320][i][1] > 64:
            strip.setPixelColor(i, Color(0,0,32))
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()


camera.stop_preview()
camera.close()

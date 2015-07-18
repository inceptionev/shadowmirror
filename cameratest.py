#test script for picamera
import picamera
import time
import picamera.array
import io
import RPi.GPIO as GPIO

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


camera.stop_preview()
camera.close()

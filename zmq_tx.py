import zmq
import time
import pickle
import numpy as np

port = 6000
zmq_context = zmq.Context()
zsock = zmq_context.socket(zmq.PUB)
zsock.bind('tcp://*:%d' % port)


imageorig = pickle.load(open( "frame.p", "rb" ))

count = 320*60*3

image2 = np.reshape(imageorig, count).tolist()

# starting from 30'th pixel, moving foward 60 pixels at a time (to arrive on the pixel "below" it)
imageslice = image2[30*3:count:60*3]



i = 0
while 1:
	obj = {}
	# obj = {'hello':'world', 'i':i}
	zsock.send(bytearray(imageslice))
	print obj
	i += 1
	#time.sleep(2)

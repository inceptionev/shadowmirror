import zmq
import time

port = 6000
zmq_context = zmq.Context()
zsock = zmq_context.socket(zmq.PUB)
zsock.bind('tcp://*:%d' % port)


i = 0
while 1:
	obj = {}
	obj = {'hello':'world', 'i':i}
	zsock.send_pyobj(obj)
	print obj
	i += 1
	#time.sleep(2)

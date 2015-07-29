import zmq


zmq_context = zmq.Context()
zsock = zmq_context.socket(zmq.SUB)
zsock.setsockopt(zmq.SUBSCRIBE, '') # empty string here subscribes to all channels
port = 6000
zsock.connect('tcp://127.0.0.1:%d' % port)

poller = zmq.Poller()
poller.register(zsock, zmq.POLLIN)



while(1):
	socks = dict(poller.poll(0))
       	if zsock in socks and socks[zsock] == zmq.POLLIN:
		msg = zsock.recv_pyobj()
		print msg

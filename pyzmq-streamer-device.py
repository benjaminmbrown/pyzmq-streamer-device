import time
import zmq
from zmq.devices.basedevice import ProcessDevice
from multiprocessing import Process

fe_port = 5559
be_port = 5560
num_workers = 5

def server():
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
	socket.connect("tcp://127.0.0.1:%d" % fe_port)
	for i in xrange(0,1000):
		socket.send("#%s" % i)
		time.sleep(0.25)

def worker(worker_number):
	context = zmq.Context()
	socket = context.socket(zmq.PULL)

	socket.connect("tcp://127.0.0.1:%d" % be_port)

	while True:
		message = socket.recv()
		print "Worker #%s got message: %s" % (worker_number, message)
		time.sleep(1)

if __name__ == "__main__":
	
	#in zmq device it takes socket objects, process device takes socket types

	
	streamer_device = ProcessDevice(zmq.STREAMER, zmq.PULL, zmq.PUSH)

	streamer_device.bind_in("tcp://127.0.0.1:%d" % fe_port)
	streamer_device.bind_out("tcp://127.0.0.1:%d" % be_port)
	streamer_device.setsockopt_in(zmq.IDENTITY, "PULL")
	streamer_device.setsockopt_out(zmq.IDENTITY, "PUSH")

	streamer_device.start()
	#creates a few workers before server starts sending
	for worker_number in range(num_workers):
		Process(target = worker, args  = (worker_number,)).start()

	time.sleep(1)

	server()
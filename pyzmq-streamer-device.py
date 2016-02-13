import time
import zmq
from zmq.devices.basedevice import ProcessDevice
from multiprocessing import ProcessDevice

fe_port = 5559
be_port = 5560

num_workers = 5

#in zmq device it takes socket objects, process device takes socket types

streamer_device = ProcessDevice(zmq.STREAMER, zmq.PULL, zmq.PUSH)

streamer_device.bind_in("tcp://127.0.0.1:%d" % fe_port)
streamer_device.bind_out("tcp://127.0.0.1:%d" % be_port)
streamer_device.setsockopt_in(zmq.IDENTITY, "PULL")
streamer_device.setsockopt_out(zmq.IDENTITY, "PUSH")

streamer_device.start()
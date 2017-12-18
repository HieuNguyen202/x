from tcp import *
from arduino import *
from queue import Queue
from struct import Struct
import time



def test1():
    arduino = Arduino(i2cAddress = 7)
    for power in range(128):
        arduino.motor(1, power)
    for power in reversed(range(128)):
        arduino.motor(1, power)

def test2():
    sq = Queue()
    rq = Queue()

    sender = TCP(isServer = True, isSender = True, host = "192.168.0.25", port = 6789, q = sq)
    receiver = TCP(isServer = True, isSender = False, host = "192.168.0.25", port = 1234, q = rq)

    sender.bind()
    receiver.bind()
    sender.start()
    receiver.start()

    arduino = Arduino(i2cAddress = 7)
    struct = Struct('BBb')
    while True:
        while not rq.empty():
            message = struct.unpack(rq.get())
            if message[0] == 1:
                arduino.motor(message[1], message[2])

test2()
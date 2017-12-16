from tcp import *
from i2c import *
from queue import Queue
from struct import Struct
import time

sq = Queue()
rq = Queue()
sStruct = Struct('B'*32)
rStruct = Struct('B'*32)
sender = TCP(isServer = True, isSender = True, host = "192.168.0.25", port = 6789, q = sq)
receiver = TCP(isServer = True, isSender = False, host = "192.168.0.25", port = 1234, q = rq)
arduino = I2C(slaveAddress=7)

sender.bind()
receiver.bind()
sender.start()
receiver.start()

while True:
    data = arduino.read(32)
    sq.put(sStruct.pack(*data))
    time.sleep(1)
    while not rq.empty():
        print(rq.get())



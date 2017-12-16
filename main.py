from i2c import *
from queue import Queue
q = Queue()
i = I2C(slaveAddress=7, isSender=True, q = q)
i.write(0, 1)
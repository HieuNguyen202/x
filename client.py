from Com import *
from queue import Queue
from collector import *
from gui import *

sq = Queue()
rq = Queue()

sender = Com(isServer = False, isSender = True, host = "192.168.0.4", port = 1234, q = sq)
receiver = Com(isServer = False, isSender = False, host = "192.168.0.4", port = 6789, q = rq)

g = GUI(rq)
c = Collector(sq)

g.start()
c.start()

sender.start()
receiver.start()

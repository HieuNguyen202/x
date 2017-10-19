from Com import *
from queue import Queue
q = Queue()
s = Com("192.168.0.4",12344, q)
s.bind()
s.start()

i = 0
while i < 1000:
    if q.empty():
        pass
    else:
        print(q.get())
        i += 1
print("exited")
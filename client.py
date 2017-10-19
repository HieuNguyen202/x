from Com import *
import time
s = Com("192.168.0.4",12344, None)
s.connect()
s.send("hieu".encode())
#time.sleep(1)
s.send("hieu".encode())
#time.sleep(1)
s.send("hieu".encode())
#print("send all")


import time
import threading
class Collector(threading.Thread):
    'Communication between two devices using python'

    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.running = True

    def run(self):
        i = 0
        while self.running:
            self.q.put(str(i))
            i += 1
            # time.sleep(0.1)
        print("Collector done")
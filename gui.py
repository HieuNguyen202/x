
import threading
class GUI(threading.Thread):
    'Communication between two devices using python'

    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            if not self.q.empty():
                print(self.q.get())
                self.q.task_done()
        print("Queue done")
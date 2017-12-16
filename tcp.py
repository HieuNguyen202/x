import socket
import threading
import time


class TCP(socket.socket, threading.Thread):
    'Communication between two devices using python'
    def __init__(self, isServer, isSender, host, port, q):
        threading.Thread.__init__(self)
        socket.socket.__init__(self)
        self.host = host
        self.port = port
        self.q = q
        self.running = True
        self.isServer = isServer
        self.isSender = isSender

    def run(self):
        while self.running:
            if self.isServer:
                self.listen()
            else:
                self.connect()
            if self.isSender:
                while self.running:
                    if not self.q.empty():
                        try:
                            self.client.send(self.q.get())
                        except:
                            break
                    else:
                        time.sleep(0.5)
            else:
                while self.running:
                    try:
                        data = self.client.recv(32)
                    except ConnectionResetError:
                        print("connection reset error")
                        break
                    if not data: break
                    for i in range(0, len(data), 32):
                        self.q.put(data[i:i+32])
                self.client.close()

    def listen(self):
        super().listen(1)
        self.client, self.address = self.accept()
        print("See ", self.address)

    def bind(self):
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # add this to reuse the port
        super().bind((self.host, self.port))

    def connect(self):
        super().connect((self.host,self.port))
        self.client = self #for a clean syntax of send() function

    def __str__(self):
        return self.host+":"+str(self.port)
import socket
import threading


class Com(socket.socket, threading.Thread):
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
                            self.client.send(self.q.get().encode())
                        except:
                            break
            else:
                while self.running:
                    data = self.client.recv(4)
                    if not data: break
                    self.q.put(data)
                self.client.close()

    def listen(self):
        super().listen(1)
        self.client, self.address = self.accept()

    def bind(self):
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # add this to reuse the port
        super().bind((self.host, self.port))

    def connect(self):
        super().connect((self.host,self.port))
        self.client = self #for a clean syntax of send() function

    def __str__(self):
        return self.host+":"+str(self.port)
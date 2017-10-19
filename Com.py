import socket
import threading


class Com(socket.socket, threading.Thread):
    'Communication between two devices using python'
    def __init__(self, host, port, q):
        threading.Thread.__init__(self)
        socket.socket.__init__(self)
        self.host = host
        self.port = port
        self.running = True
        self.q = q

    def run(self):
        while self.running:
            self.listen()
            while self.running:
                data = self.client.recv(4)
                if not data: break
                self.q.put(data)
            self.client.close()
            self.q.put("Connection closed")

    def listen(self):
        self.q.put("Listening to new connections...")
        super().listen(1)
        self.client, self.address = self.accept()
        self.q.put("Connected to " + str(self.address))

    def bind(self):
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # add this to reuse the port
        super().bind((self.host, self.port))

    def connect(self):
        super().connect((self.host,self.port))

    def __str__(self):
        return self.host+":"+str(self.port)
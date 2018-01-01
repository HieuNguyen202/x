import socket
import threading
from time import sleep
from struct import Struct
from constants import *
from queue import Queue

class TCP(socket.socket, threading.Thread):
    'Communication between two devices using python'
    def __init__(self, host, port, q):
        threading.Thread.__init__(self)
        socket.socket.__init__(self)
        self.dataStruct = Struct(DATA_STRUCTURE)
        self.commandStruct = Struct(COMMAND_STRUCTURE)
        self.host = host
        self.port = port
        self.q = q
        self.running = True
        self.client = None
        
    def appendChecksum(self, data):
        data.append((256-sum(data))%256) #add all element must get 0

    def __str__(self):
        return self.host+":"+str(self.port) +" is running: "+str(self.running)

    def doSenderTask(self):
        while self.running:
            if not self.q.empty():
                data = self.q.get()
                if data is None:
                    self.clean()
                    break
                else:
                    try:
                        self.client.send(data)
                        self.q.task_done()
                    except:
                        self.clean()
                        print("Sender send error")
                        break
            else:
                sleep(0.0001)

    def doReceiverTask(self):
        self.settimeout(0.1)
        while self.running:
            try:
                data = self.client.recv(1024)
            except ConnectionResetError:
                print("Receiver connection reset error")
                break
            except socket.timeout:
                #print("Receiver Time out")
                continue
            if not data:
                print("Receiver remote host closed properly")
                break
            self.q.put(data)
        self.settimeout(None)
        self.clean()

    def stop(self):
        self.running = False;

class TCPServer(TCP):
    'Communication between two devices using python'
    def __init__(self, host, port, sq, rq, isSender):
        if isSender:
            super().__init__(host, port, sq)
        else:
            super().__init__(host, port, rq)
        self.isSender = isSender
        self.rq = rq
        self.sq = sq
        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # add this to reuse the port
        self.bind((self.host, self.port))

    def run(self):
        while self.running:
            self.listen()
            if self.isSender:
                self.doSenderTask()
            else:
                self.doReceiverTask()

    def listen(self):
        super().listen()
        self.client, self.address = self.accept()
        self.connected()

    def disconnect(self):
        self.client.close()
        self.close()
        self.disconnected()

    def pack(self, data):
        lenDiff = DATA_LENGTH - (len(data) + 1)
        if lenDiff < 0:
            return None
        else:
            for i in range(lenDiff):
                data.append(0)
            self.appendChecksum(data)
            return self.dataStruct.pack(*data)
        
    def unpack(self, dataBin):
        return self.commandStruct.unpack(dataBin)

    def clean(self):
        if not self.isSender:
            self.sq.put(None)
        self.client.close()
        self.disconnected()
        
    def disconnected(self):
        address = self.address[0]
        self.rq.put(self.pack([0, 0, int(address.split('.')[3])]))

    def connected(self):
        address = self.address[0]
        self.rq.put(self.pack([0, 1, int(address.split('.')[3])]))

class TCPClient(TCP):
    'Communication between two devices using python'
    def __init__(self, host, port, sq, rq, isSender):
        if isSender:
            super().__init__(host, port, sq)
        else:
            super().__init__(host, port, rq)
        self.isSender = isSender
        self.rq = rq
        self.sq = sq

    def run(self):
        self.connect()
        if self.isSender:
            self.doSenderTask()
        else:
            self.doReceiverTask()
        self.disconnect()
    def connect(self):
        self.settimeout(2)
        while self.running:
            try:
                super().connect((self.host,self.port))
                self.client = self #for a clean syntax of send() function
                self.connected()
                self.settimeout(None)
                break
            except ConnectionRefusedError:
                print("Connection refused error")
            except socket.timeout:
                print("connect timeout")
                continue
        
    def disconnect(self):
        self.sq.put(None)
        self.close()
        self.disconnected()
        
    def pack(self, data):
        lenDiff = COMMAND_LENGTH - (len(data) + 1)
        if lenDiff < 0:
            return None
        else:
            for i in range(lenDiff):
                data.append(0)
            self.appendChecksum(data)
            return self.commandStruct.pack(*data)

    def clean(self):
        pass

    def unpack(self, dataBin):
        return self.dataStruct.unpack(dataBin)

    def disconnected(self):
        address = self.host
        self.rq.put(self.pack([0, 0, int(address.split('.')[3])]))

    def connected(self):
        address = self.host
        self.rq.put(self.pack([0, 1, int(address.split('.')[3])]))

class BiDirectionalTCP(object):
    """Multithreading implimentation of bi diractional TCP: sender and receiver."""
    def __init__(self, ipAddress, isServer):
        self.dataStruct = Struct(DATA_STRUCTURE)
        self.commandStruct = Struct(COMMAND_STRUCTURE)
        self.sq = Queue()
        self.rq = Queue()
        self.isServer = isServer
        self.sender = None
        self.receiver = None
        self.ipAddress =ipAddress
        

    def start(self, ipAddress = None):
        if ipAddress == None:
            ipAddress = self.ipAddress
        if self.isServer:
            self.sender = TCPServer(host = ipAddress, port = DATA_PORT, sq = self.sq, rq = self.rq, isSender = True)
            self.receiver = TCPServer(host = ipAddress, port = COMMAND_PORT, sq = self.sq, rq = self.rq, isSender = False)
        else:
            self.sender = TCPClient(host = ipAddress, port = COMMAND_PORT, sq = self.sq, rq = self.rq, isSender = True)
            self.receiver = TCPClient(host = ipAddress, port = DATA_PORT, sq = self.sq, rq = self.rq, isSender = False)
        self.sender.start()
        self.receiver.start()

    def stop(self):
        while not self.sq.empty():
            sleep(0.01)
        self.sender.stop()
        self.receiver.stop()
        sleep(0.1)
        self.sender.disconnect()
        self.receiver.disconnect()
        sleep(0.1)
        self.sender.join()
        self.receiver.join()

    def send(self, data):
        self.sq.put(data)

    def pack(self, data):
        return self.sender.pack(data)

    def unpack(self, data):
        return self.sender.unpack(data)

class Robot(BiDirectionalTCP):
    def __init__(self, ipAddress):
        super().__init__(ipAddress = ipAddress, isServer = False)

    def motor(self, device, value):
        self.send(self.pack([1, device, value]))

    def getNewInfo(self): # only return valid data
        if not self.rq.empty():
            data = self.rq.get() #get binary data from receiver queue
            def iter():
                for i in range(0, len(data), DATA_LENGTH):
                    dataList = self.unpack(data[i: i + DATA_LENGTH])
                    if sum(dataList)%256 == 0: #check sum
                        yield dataList
            return iter()
        else:
            return None

class Controller(BiDirectionalTCP):
    def __init__(self, ipAddress):
        super().__init__(ipAddress = ipAddress, isServer = True)

    def getNewCommands(self): # only return valid data
        if not self.rq.empty():
            data = self.rq.get() #get binary data from receiver queue
            def iter():
                for i in range(0, len(data), COMMAND_LENGTH):
                    dataList = self.unpack(data[i: i + COMMAND_LENGTH])
                    if sum(dataList)%256 == 0: #check sum
                        yield dataList
            return iter()
        else:
            return None
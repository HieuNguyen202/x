from tcp import *
from queue import Queue
from collector import *
from gui import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from struct import Struct

sq = Queue()
rq = Queue()
app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
sStruct = Struct('B'*32)

def initGUI():    
    ui.setupUi(gui)
    guiTimer = QtCore.QTimer()
    guiTimer.timeout.connect(updateRobotInfo)
    guiTimer.start(1000)
    commandTimer = QtCore.QTimer()
    commandTimer.timeout.connect(sendCommand)
    commandTimer.start(1000)

    ui.pushButtonForward.pressed.connect(forward)
    ui.pushButtonForward.released.connect(stop)
    ui.pushButtonReverse.pressed.connect(reverse)
    ui.pushButtonReverse.released.connect(stop)
    ui.pushButtonStop.pressed.connect(stop)
    ui.actionConnect.triggered.connect(initTCP)
    ui.sliderSpeedControl.valueChanged.connect(lineEditUpdateSpeed)
    ui.lineEditMotorSpeed.setText("100")
    gui.show()
    sys.exit(app.exec_())

count = 0
def sendCommand():
    global count
    data = [count]*32
    sq.put(sStruct.pack(*data))
    count += 1
    if count > 128:
        count = 0

def updateRobotInfo():
    while not rq.empty():
        print(rq.get())

def hieu():
    print("hieu")

def initTCP():
    sender = TCP(isServer = False, isSender = True, host = "192.168.0.25", port = 1234, q = sq)
    receiver = TCP(isServer = False, isSender = False, host = "192.168.0.25", port = 6789, q = rq)
    sender.start()
    receiver.start()

def lineEditUpdateSpeed(speed):
    speed = str(speed)
    ui.lineEditMotorSpeed.setText(speed)


def forward():
    speed = ui.sliderSpeedControl.value()
    tcpSend(1,speed)

def reverse():
    speed = ui.sliderSpeedControl.value()
    tcpSend(2,speed)

def stop():
    tcpSend(0,0)

def tcpSend(command, value):
    m.update([command,value])
    sq.put(m.encode('tcp'))

initGUI()






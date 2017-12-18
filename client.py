from tcp import *
from queue import Queue
from gui import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from struct import Struct
from robot import Robot

"""
Commands:
    1: drive motors

"""


sq = Queue()
rq = Queue()
app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
struct = Struct('BBb')
robot = Robot(sq, rq)

pressedButton = -1

def initGUI():    
    ui.setupUi(gui)
    #guiTimer = QtCore.QTimer()
    #guiTimer.timeout.connect(updateRobotInfo)
    #guiTimer.start(1000)
    #commandTimer = QtCore.QTimer()
    #commandTimer.timeout.connect(tcpTest)
    #commandTimer.start(1000)

    #Connect signals
    ui.pushButtonForward.pressed.connect(forwardPressed)
    ui.pushButtonForward.released.connect(forwardReleased)
    ui.pushButtonReverse.pressed.connect(reversePressed)
    ui.pushButtonReverse.released.connect(reverseReleased)
    ui.pushButtonStop.pressed.connect(stop)
    ui.actionConnect.triggered.connect(initTCP)
    ui.sliderSpeedControl.valueChanged.connect(lineEditUpdateSpeed)

    app.aboutToQuit.connect(close)
    currentSliderValue = str(ui.sliderSpeedControl.value())
    ui.lineEditMotorSpeed.setText(currentSliderValue)

    initTCP() #auto connect at startup

    gui.show()
    sys.exit(app.exec_())

count = 0
def tcpTest():
    global count
    data = [count]*32
    sq.put(sStruct.pack(*data))
    count += 1
    if count > 128:
        count = 0


def initTCP():
    global sender
    global receiver
    sender = TCP(isServer = False, isSender = True, host = "192.168.0.25", port = 1234, q = sq)
    receiver = TCP(isServer = False, isSender = False, host = "192.168.0.25", port = 6789, q = rq)
    sender.start()
    receiver.start()

def lineEditUpdateSpeed(speed):
    speed = str(speed)
    ui.lineEditMotorSpeed.setText(speed)
    if pressedButton == -1:
        reversePressed()
    elif pressedButton == 1:
        forwardPressed()
    else:
        pass

def forwardPressed():
    global pressedButton
    power = ui.sliderSpeedControl.value()
    robot.motor(motorID = 1, power = power)
    pressedButton = 1

def reversePressed():
    global pressedButton
    power = ui.sliderSpeedControl.value()
    robot.motor(motorID = 1, power = - power)
    pressedButton = -1

def forwardReleased():
    if not ui.checkBoxStickyMode.isChecked():
        stop()

def reverseReleased():
    if not ui.checkBoxStickyMode.isChecked():
        stop()  

def stop():
    global pressedButton
    robot.motor(motorID = 1, power = 0)
    pressedButton = 0

def close():
    stop()
    while not rq.empty():
        time.sleep(0.01)
    while not sq.empty():
        time.sleep(0.01)
    sender.running = False
    receiver.running = False
    sender.join()
    receiver.join()
    app.exit()
    sys.exit()
initGUI()






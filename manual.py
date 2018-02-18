import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from tcp import Robot
from manualGUI import Ui_Manual

gear = [20, 40, 60, 80, 100]

drive = 50
turn = 0
robot = Robot(ipAddress = "127.0.0.1")

def connect():
    robot.start()

def disconnect():
    pass

def forward():
    robot.drive(drive = drive, turn = turn)

def backward():
    robot.drive(drive = -drive, turn = turn)

def right():
    global drive; global turn
    setTurn(100)
    ui.horizontalSlider_5.setValue(100)
    robot.drive(drive, turn)

def left():
    setTurn(-100)
    ui.horizontalSlider_5.setValue(-100)
    robot.drive(drive, turn)

def stop():
    setTurn(0)
    ui.horizontalSlider_5.setValue(0)
    robot.drive(drive = 0, turn = turn)

def setDrive(newDrive):
    global drive
    drive = newDrive
    ui.blank_6.setText(str(newDrive))
    
def setTurn(newTurn):
    global turn
    turn = newTurn
    ui.blank_5.setText(str(newTurn))

def decrementDrive():
    global gear, drive
    for newDrive in reversed(gear):
        if newDrive < drive:
            ui.verticalSlider.setValue(newDrive)
            setDrive(newDrive)
            break

def incrementDrive():
    global gear, drive
    for newDrive in gear:
        if newDrive > drive:
            ui.verticalSlider.setValue(newDrive)
            setDrive(newDrive)
            break

def connectSignalAndSlot():
    ui.forwardButton.pressed.connect(forward)
    ui.forwardButton.released.connect(stop)
    ui.backButton.pressed.connect(backward)
    ui.backButton.released.connect(stop)
    ui.rightButton.pressed.connect(right)
    ui.rightButton.released.connect(stop)
    ui.leftButton.pressed.connect(left)
    ui.leftButton.released.connect(stop)
    ui.stopButton.pressed.connect(robot.stopAll)
    ui.verticalSlider.valueChanged.connect(lambda: setDrive(ui.verticalSlider.value()))
    ui.horizontalSlider_5.valueChanged.connect(lambda: setTurn(ui.horizontalSlider_5.value()))

app = QtWidgets.QApplication(sys.argv)
gui = QtWidgets.QMainWindow()
ui = Ui_Manual()
ui.setupUi(gui)
connectSignalAndSlot()
connect()
gui.show()
sys.exit(app.exec_())
from tcp import Controller
from time import sleep

pc = Controller("192.168.0.6")
pc.start()

while 1:
    commands = pc.getNewCommands()
    if  commands is not None:
        for command in commands:
            print(command)




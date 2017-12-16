"""
#have to run 'sudo apt-get install python-smbus'
#in Terminal to install smbus
import smbus as smbus
#handle error when data slave is unavailable
"""
import smbus2

class I2C(smbus2.SMBus):
    def __init__(self, slaveAddress):
        super().__init__(1)
        self.slaveAddress=slaveAddress

    def write(self, command, data):
        if not isinstance(data,list):
            data=[data,]
        self.write_i2c_block_data(self.slaveAddress, command, data)
        #time.sleep(0.01)#must delay 0.01 second

    def read(self, numBytes):
        return self.read_i2c_block_data(self.slaveAddress, 0, numBytes)

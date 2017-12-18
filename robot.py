"""
commands:
1: drive motors
"""
from struct import Struct

class Robot(object):
    def __init__(self, sq, rq):
        self.sq = sq
        self.rq = rq
        self.struct = Struct('BBb') #command, selector, value

    def motor(self, motorID, power):
        self.sq.put(self.struct.pack(1, motorID, power))

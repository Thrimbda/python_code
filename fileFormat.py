import os
import numpy as np


class FileFomate():
    def __init__(self, rfileName, wfileName, startLine=0, endLine=-1):
        try:
            self.rfileobj = open(rfileName, 'r')
            self.wfileobj = open(wfileName, 'w')
            self.data = self.rfileobj.readlines()[startLine:endLine]
        except IOError:
            print("faile to open file. please check your file name.")

    def encoderFmt(self):
        for line in self.data:
            line = line.replace('(', '').replace(')', '').replace(',', '') + '\n'
            self.wfileobj.write(line)

    def pointRouteFmt(self):
        for line in self.data:
            line = line.replace('{', '').replace('}', '').replace(' ', '') + '\n'
            self.wfileobj.write(line)

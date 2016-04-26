import numpy as np


class FileFomate():
    """my fomate script.

    fomate files into specific type.

    Variables:
        ff.encoderFmt() {[none]} -- [for matlab]
        ff.pointRouteFmt() {[none]} -- [for myConsole]
    """
    def __init__(self, rfileName, wfileName, startLine=0, endLine=-1):
        try:
            self.rfileobj = open(rfileName, 'r', encoding="gb2312")
            self.wfileobj = open(wfileName, 'w')
            self.data = self.rfileobj.readlines()[startLine:endLine]
        except IOError:
            print("faile to open file. please check your file name.")

    def encoderFmt(self):
        for line in self.data:
            line = line.replace('(', '').replace(')', '').replace(',', '') + '\n'
            self.wfileobj.write(line)
        self.rfileobj.close()
        self.wfileobj.close()

    def pointRouteFmt(self):
        for line in self.data:
            line = line.replace('{', '').replace('}', '').replace(' ', '').split(',')
            line = '(' + line[0] + ',' + line[1] + ',' + line[2] + ',' + str(np.cos(eval(line[4]) * eval(line[2]))) + ',' + str(np.sin(eval(line[4]) * eval(line[2]))) + ',' + line[4] + ')\n'
            self.wfileobj.write(line)
        self.rfileobj.close()
        self.wfileobj.close()

if __name__ == '__main__':
    ff = FileFomate('/home/michael/Documents/python_code/PointRoute.c', '/home/michael/Documents/python_code/Fmt_blue.c', 10, 4230)
    ff.pointRouteFmt()


import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
import sys
from test import *
import time
import os
import binascii
basedir = os.getcwd()

import struct
import socket
import serial
import subprocess
import numpy as np
datatype = np.dtype([('x', '<f'), ('y', '<f')])
try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
i = 0
line = None

try:
    subprocess.Popen('plot2', shell=False)
except Exception:
    pass


class worker(QThread):
    def __init__(self, window):
        QThread.__init__(self, None)
        self.window = window

    def run(self):
        global i
        while 1:
            time.sleep(0.8)
            if self.window.is_open:
                num2read = self.window.comm.inWaiting()
                if num2read == 0:
                    continue
                data = self.window.comm.read(num2read)
                if len(data) > 0:
                    self.window.update(data)


class TestDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        self.setupUi(self)
        self.available_port = []
        self.get_available_port()
        self.spliter = ''
        self.is_open = False
        self.is_save_to_file = False
        self.comm = None
        self.closecomm.setDisabled(True)
        self.framelenth = 0
        self.connect(self.opencomm, SIGNAL('clicked()'), self.open_comm)
        self.connect(self.closecomm, SIGNAL('clicked()'), self.close_comm)
        self.connect(self.path, SIGNAL('clicked()'), self.get_path)
        self.content = ''
        self.fmt = ''
        self.point_x = []
        self.point_y = []
        self.lastpoint = 0
        try:
            self.configfile = open(basedir + '\\config', 'r')
            config = self.configfile.read(-1).split(',')
            self.configfile.close()
            self.format_edit.setText(config[2])
            self.spliter_edit.setText(config[0])
            self.framele_edit.setText(config[1])
        except Exception:
            pass
        self.filepath_edit.setText(basedir+'\data')
        self.filepath = basedir+'\data'
        self.rawdatafile = None
        self.logfile = None
        self.sock = None
        self.counter = 0

    def get_available_port(self):
        for i in range(10):
            try:
                s = serial.Serial(i)
                self.available_port.append(i)
                s.close()
            except Exception:
                pass
        for i in range(len(self.available_port)):
            self.comboBox.addItem(_fromUtf8(""))
            self.comboBox.setItemText(i, 'COM'+str(self.available_port[i]+1))

    def open_comm(self):
        try:
            try:
                spliter = self.spliter_edit.text()
                if len(spliter) % 2 == 1 or len(spliter) == 0:
                    QMessageBox.warning(self, "warning", 'the lenth should be a even number')
                    return
                self.spliter = binascii.a2b_hex(str(spliter))
                self.framelenth = int(self.framele_edit.text())
                self.fmt = str(self.format_edit.text())
            except Exception:
                QMessageBox.warning(self, "warning", 'please give a right spliter')
                return
            try:
                self.rawdatafile = open(basedir + '\\rawdata', 'w')
                self.filepath = str(self.filepath_edit.text())
                self.logfile = open(basedir + '\\data', 'w')
            except Exception:
                QMessageBox.warning(self, 'warning', 'fail to open file')
                return

            self.configfile = open(basedir + '\\config', 'w')
            self.configfile.write(spliter+','+str(self.framelenth)+','+self.fmt)
            self.configfile.close()

            comm_num = self.comboBox.currentIndex()
            self.comm = serial.Serial(self.available_port[comm_num], baudrate=115200)
            self.is_open = True
            self.opencomm.setDisabled(True)
            self.comboBox.setDisabled(True)
            self.baud.setDisabled(True)
            self.closecomm.setDisabled(False)
            self.framele_edit.setDisabled(True)
            self.spliter_edit.setDisabled(True)
            self.format_edit.setDisabled(True)
            f = open('point', 'w')
            f.close()
        except:
            print('open error')
        print("open")

    def close_comm(self):
        try:
            self.is_open = False
            time.sleep(0.1)
            self.comm.close()
            self.rawdatafile.close()
            self.opencomm.setDisabled(False)
            self.comboBox.setDisabled(False)
            self.baud.setDisabled(False)
            self.closecomm.setDisabled(True)
            self.framele_edit.setDisabled(False)
            self.spliter_edit.setDisabled(False)
            self.format_edit.setDisabled(False)
            self.logfile.close()
        except:
            print('close error')

    def get_path(self):
        s = QFileDialog.getExistingDirectory(self, "Open file dialog", basedir)
        self.filepath_edit.setText(str(s).replace('/', '\\') + '\data')

    def update(self, data):
        self.rawdatafile.write(data)
        self.content = self.content + data
        if len(self.content) <= self.framelenth:
            return
        frm = self.content.split(self.spliter)
        for i in range(len(frm)):
            if len(frm[i]) == self.framelenth - len(self.spliter):
                self.counter = (self.counter + 1) % 3
                if self.counter == 0:
                    self.display(frm[i])
            elif len(frm[i]) <= self.framelenth:
                continue
        self.content = frm[len(frm) - 1]

    def display(self, data):
        dip = struct.unpack(self.fmt, data)
        self.logfile.write(str(dip)+'\n')
        f = open('point', 'a')
        f.write(str(dip)+'\n')
        f.close()
        #print dip
        #print dip
        # self.point_x.append(dip[0])
        # self.point_y.append(dip[1])
        # f = open('E:\point_x','w')
        # f.write(str(self.point_x).replace('[','').replace(']',''))
        # f.close()
        # f = open('E:\point_y','w')
        # f.write(str(self.point_y).replace('[','').replace(']',''))
        # f.close()

        # if self.counter == 0:
        #     self.logfile.write('\n')
        # try:
        #     self.sock.sendall(data)
        # except Exception:
        #     # try:
        #         self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #         self.sock.connect(('127.0.0.1',50007))
app = QApplication(sys.argv)

dialog = TestDialog()

work = worker(dialog)
work.start()
dialog.show()
app.exec_()

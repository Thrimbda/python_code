#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-16 16:36:30
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-04-14 20:42:29
import matplotlib       #绘图库
matplotlib.use('Qt5Agg')        #qt5接口声明
from PyQt5 import QtGui, QtCore, QtWidgets      #qt
import sys
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt         #绘图模块
import matplotlib.animation as animation        #动画模块
import matplotlib.gridspec as gridspec          #分块模块
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT          #图接口以及工具库
# implement the default mpl key bindings
import mec_acc
import serial       #串口模块
import os.path
import platform
import struct
# import threading
import time

pf = platform.system()      #识别当前工作环境


class SerialCtl():      #serial Initialization
    def __init__(self):
        self.available_port = []
        self.ser = None

    def serialInit(self, port):     #串口模块初始化
        try:
            self.ser = serial.Serial(port, baudrate=115200, timeout=0)
        except Exception:
            return False
        else:
            return True

    def serialClose(self):
        self.ser.close()

    def getAvailablePort(self):
        for i in np.arange(99):
            try:
                if pf == 'Windows':
                    s = serial.Serial('COM' + str(i))
                    self.available_port.append('COM' + str(i))
                elif pf == 'Linux':
                    s = serial.Serial('/dev/ttyUSB' + str(i))
                    self.available_port.append('/dev/ttyUSB' + str(i))
                s.close()
            except Exception:
                pass

    def readline(self):
        try:
            return self.ser.readline()
        except serial.SerialException:
            raise serial.SerialException

    def writeCmd(self, string):
        string = eval(string)
        string = struct.pack("H", string)
        self.ser.write(string)


class Graph():
    def __init__(self, width=30, height=10, dpi=80, xmin=-14000,
                 xmax=0, ymin=0, ymax=14000):
        self.ser = SerialCtl()
        self.serRead = b''
        self.t = 0
        # 对整个图进行分区2列x4行
        self.subs = gridspec.GridSpec(2, 6)
        self.fig = plt.Figure(  #facecolor = "black",
                          figsize=(width, height), dpi=dpi)        #设定图大小20英寸x10英寸
        # 对图进行分割
        self.ax1 = self.fig.add_subplot(self.subs[:, 2:4])
        self.ax2 = self.fig.add_subplot(self.subs[0, 0], projection='polar')
        self.ax3 = self.fig.add_subplot(self.subs[1, 0])
        self.ax4 = self.fig.add_subplot(self.subs[0, 1])
        self.ax5 = self.fig.add_subplot(self.subs[1, 1])
        self.axFl = self.fig.add_subplot(self.subs[0, 4])
        self.axFr = self.fig.add_subplot(self.subs[1, 4])
        self.axBl = self.fig.add_subplot(self.subs[0, 5])
        self.axBr = self.fig.add_subplot(self.subs[1, 5])
        # import image
        # self.imagefile = cbook.get_sample_data(os.path.split(os.path.realpath(__file__))[0]+'/map.png')
        # self.image = plt.imread(self.imagefile)
        # self.im = self.ax1.imshow(self.image)
        # 设定各子图标题
        self.ax1.set_title("Cart's route")
        self.ax2.set_title("Angle")
        self.ax3.set_title("speed:X")
        self.ax4.set_title("speed:Y")
        self.ax5.set_title("speed:total")
        self.axFl.set_title("Fl-rotation")
        self.axFr.set_title("Fr-rotation")
        self.axBl.set_title("Bl-rotation")
        self.axBr.set_title("Br-rotation")
        # 初始化并设定各子图样式
        self.route, = self.ax1.plot([], [], 'g-', lw=2)     #lw is linewidth
        self.stdB_route, = self.ax1.plot([], [], 'b-', lw=2)
        self.stdR_route, = self.ax1.plot([], [], 'r-', lw=2)
        self.angle, = self.ax2.plot([], [], 'b-', lw=2)

        # self.speed_x, = self.ax3.plot([], [], 'b-', lw=2)
        # self.speed_y, = self.ax4.plot([], [], 'b-', lw=2)
        # self.speed, = self.ax5. plot([], [], 'b-', lw=2)

        self.lowPassSpeed_x, = self.ax3.plot([], [], 'g-', lw=2)
        self.lowPassSpeed_y, = self.ax4.plot([], [], 'g-', lw=2)
        self.lowPassSpeed, = self.ax5.plot([], [], 'g-', lw=2)

        self.fl, = self.axFl.plot([], [], 'g-', lw=2)
        self.fr, = self.axFr.plot([], [], 'g-', lw=2)
        self.bl, = self.axBl.plot([], [], 'g-', lw=2)
        self.br, = self.axBr.plot([], [], 'g-', lw=2)

        # 设定路径图长宽
        self.ax1.set_xlim(xmin, xmax)
        self.ax1.set_ylim(ymin, ymax)
        # 对各图数据初始化
        (self.optimalX_data, self.optimalY_data, self.encoder1_data,
         self.encoder2_data, self.stdB_X_data, self.stdB_Y_data,
         self.stdR_X_data, self.stdR_Y_data, self.X_data,
         self.Y_data, self.A_data, self.Speed_X_data,
         self.optimalColSpeed_data, self.optimalVerSpeed_data, self.optimalSpeed_data,
         self.Speed_Y_data, self.Speed_data, self.t_data,
         self.optimalRotSpeed_data, self.flRot, self.frRot,
         self.blRot, self.brRot, self.Rotation) = ([], [], [],
                                                   [], [], [],
                                                   [], [], [],
                                                   [], [], [],
                                                   [], [], [],
                                                   [], [], [],
                                                   [], [], [],
                                                   [], [], [])
        self.timeNode = []
        # 打开文件
        with open(os.path.split(os.path.realpath(__file__))[0] +
                  '/Fmt_RouteBlue.txt', 'r') as self.stdB_fobj:
            self.database = self.stdB_fobj.readlines()
        for item in self.database:
            self.info = tuple(eval(item))
            (self.stdB_X, self.stdB_Y, self.stdB_A,
             self.stdB_Speed_X, self.stdB_Speed_Y, self.stdB_Speed) = self.info
            self.stdB_X_data.append(self.stdB_X)
            self.stdB_Y_data.append(-self.stdB_Y)
        self.stdB_route.set_data(self.stdB_X_data, self.stdB_Y_data)

        for item in range(0, len(self.database)):
            self.stdR_X_data.append(-self.stdB_X_data[item]-14000)
            self.stdR_Y_data.append(self.stdB_Y_data[item])
        self.stdR_route.set_data(self.stdR_X_data, self.stdR_Y_data)

        self.ax2.set_ylim(0, 50)
        self.ax3.set_xlim(0, 50)
        self.ax3.set_ylim(-3000, 3000)
        self.ax4.set_xlim(0, 50)
        self.ax4.set_ylim(-3000, 3000)
        self.ax5.set_xlim(0, 50)
        self.ax5.set_ylim(0, 3000)
        self.axFl.set_xlim(0, 50)
        self.axFl.set_ylim(-44.8, 44.8)
        self.axFr.set_xlim(0, 50)
        self.axFr.set_ylim(-44.8, 44.8)
        self.axBl.set_xlim(0, 50)
        self.axBl.set_ylim(-44.8, 44.8)
        self.axBr.set_xlim(0, 50)
        self.axBr.set_ylim(-44.8, 44.8)

        self.fig.tight_layout()

        # Filter params
        self.signalGain, self.bandwidth = signal.butter(5, 0.30, 'low')
        print(self.signalGain, self.bandwidth)

    def speedCalculator(self, col_data, ver_data, rot_data,
                        colSpeed_data, verSpeed_data, rotSpeed_data,
                        speed_data):
        if len(self.t_data) < 3:
            colSpeed = verSpeed = rotSpeed = speed = 0
            return colSpeed, verSpeed, rotSpeed, speed
        elif self.t_data[-1] - self.t_data[-2] == 0:
            colSpeed = colSpeed_data[-1]
            verSpeed = verSpeed_data[-1]
            rotSpeed = rotSpeed_data[-1]
            speed = speed_data[-1]
            return colSpeed, verSpeed, rotSpeed, speed
        else:
            colSpeed = ((col_data[-1] - col_data[-2]) /
                        (self.t_data[-1] - self.t_data[-2]))
            verSpeed = ((ver_data[-1] - ver_data[-2]) /
                        (self.t_data[-1] - self.t_data[-2]))
            rotSpeed = ((rot_data[-1] - rot_data[-2]) /
                        (self.t_data[-1] - self.t_data[-2]))
            speed = np.sqrt(colSpeed ** 2 + verSpeed ** 2)
            return colSpeed, verSpeed, rotSpeed, speed

    def timeCount(self):
        if len(self.timeNode) != 0:
            timeRecord = []
            for i in range(len(self.timeNode)):
                if i == 0:
                    timeRecord.append("大车路径点记录：\n第%.1f秒大车启动\n" % (self.timeNode[i]))
                else:
                    timeRecord.append("第%d段路径用时%.1f秒\n" % (i, self.timeNode[i]-self.timeNode[i-1]))
            if len(self.timeNode) == 19:
                timeRecord.append("路径用时%.1f秒，寻杆用时%.1f秒\n总计用时%.1f秒" %
                                  (self.timeNode[17]-self.timeNode[0],
                                   self.timeNode[18]-self.timeNode[17],
                                   self.timeNode[18]-self.timeNode[0]))
            else:
                timeRecord.append("总计用时%.1f秒" % (self.timeNode[-1]-self.timeNode[0]))
        else:
            timeRecord = ["no data in the record"]
        timeRecord = ''.join(timeRecord)
        return timeRecord

    def init(self):         # 动画初始化

        self.route.set_data([], [])
        self.angle.set_data([], [])

        self.lowPassSpeed_x.set_data([], [])
        self.lowPassSpeed_y.set_data([], [])
        self.lowPassSpeed.set_data([], [])
        self.fl.set_data([], [])
        self.fr.set_data([], [])
        self.bl.set_data([], [])
        self.br.set_data([], [])

        return (self.stdR_route, self.stdB_route, self.route,
                self.angle, self.lowPassSpeed_x, self.lowPassSpeed_y,
                self.lowPassSpeed, self.fl, self.fr,
                self.bl, self.br)

    def clear(self):
        (self.t_data, self.X_data, self.Y_data,
         self.A_data, self.Speed_X_data, self.Speed_Y_data,
         self.Speed_data, self.optimalColSpeed_data, self.optimalVerSpeed_data,
         self.optimalRotSpeed_data, self.optimalSpeed_data, self.timeNode,
         self.flRot, self.frRot, self.blRot,
         self.brRot, self.Rotation) = ([], [], [],
                                       [], [], [],
                                       [], [], [],
                                       [], [], [])
        self.ax2.set_ylim(0, 50)
        self.ax3.set_xlim(0, 50)
        self.ax4.set_xlim(0, 50)
        self.ax5.set_xlim(0, 50)
        self.axFl.set_xlim(0, 50)
        self.axFl.set_xlim(0, 50)
        self.axBl.set_xlim(0, 50)
        self.axBl.set_xlim(0, 50)
        self.ax2.figure.canvas.draw()
        self.ax3.figure.canvas.draw()
        self.ax4.figure.canvas.draw()
        self.ax5.figure.canvas.draw()
        self.axFl.figure.canvas.draw()
        self.axFl.figure.canvas.draw()
        self.axBl.figure.canvas.draw()
        self.axBl.figure.canvas.draw()
        self.init()

    def generator(self):      # 数据迭代器
        while True:
            try:
                self.serRead = self.ser.readline()
            except serial.SerialException:
                raise serial.SerialException
            if self.serRead == b'':
                (self.X, self.Y, self.A,
                 self.Speed_X, self.Speed_Y, self.Speed) = (None, None, None,
                                                            None, None, None)
                yield self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed
                # this yield is very importent. without it the program will get into a endless loop here.
            else:
                try:
                    self.info = tuple(eval(self.serRead))
                    if self.info[-1] == 2:
                        self.timeNode.append(self.info[0])
                        print(self.timeNode)
                        raise Exception
                    elif self.info[-1] != 1 and self.info[-1] != 2:
                        raise Exception
                except Exception:
                    self.type = 'bad_datatype'
                    print(self.type, self.info)
                else:
                    self.X, self.Y, self.A, self.t = self.info[0], self.info[1], self.info[2], self.info[-2]
                    self.encoder1, self.encoder2 = self.info[3], self.info[4]
                    (self.Speed_X,
                     self.Speed_Y,
                     self.Speed_R,
                     self.Speed) = self.speedCalculator(self.X_data,
                                                        self.Y_data,
                                                        self.A_data,
                                                        self.optimalColSpeed_data,
                                                        self.optimalVerSpeed_data,
                                                        self.optimalRotSpeed_data,
                                                        self.optimalSpeed_data)
                    # self.kalmanFilter()
                    # self.optimalColSpeed, self.optimalVerSpeed, self.optimalSpeed = self.speedCalculator(self.optimalX_data, self.optimalY_data, self.optimalColSpeed_data, self.optimalVerSpeed_data, self.optimalVerSpeed_data)

                    fl, fr, bl, br = mec_acc.set_speed(self.Speed_X, self.Speed_Y, self.Speed_R)
                    self.t_data.append(self.t)
                    self.X_data.append(self.X)
                    self.Y_data.append(self.Y)
                    self.A_data.append(self.A)
                    self.flRot.append(fl)
                    self.frRot.append(fr)
                    self.blRot.append(bl)
                    self.brRot.append(br)
                    self.encoder1_data.append(self.encoder1)
                    self.encoder2_data.append(self.encoder2)
                    self.Speed_X_data.append(self.Speed_X)
                    self.Speed_Y_data.append(self.Speed_Y)
                    self.Rotation.append(self.Speed_R)
                    self.Speed_data.append(self.Speed)

                    # self.optimalX_data.append(self.optimalX)
                    # self.optimalY_data.append(self.optimalY)
                    if (len(self.t_data)) < 19:
                        self.optimalColSpeed_data = self.Speed_X_data
                        self.optimalVerSpeed_data = self.Speed_Y_data
                        self.optimalRotSpeed_data = self.Rotation
                        self.optimalSpeed_data = self.Speed_data
                    else:
                        self.optimalColSpeed_data = signal.filtfilt(self.signalGain,
                                                                    self.bandwidth,
                                                                    self.Speed_X_data)
                        self.optimalVerSpeed_data = signal.filtfilt(self.signalGain,
                                                                    self.bandwidth,
                                                                    self.Speed_Y_data)
                        # self.optimalRotSpeed_data = signal.filtfilt(self.signalGain,
                        #                                             self.bandwidth,
                        #                                             self.Rotation)
                        self.optimalSpeed_data = signal.filtfilt(self.signalGain,
                                                                 self.bandwidth,
                                                                 self.Speed_data)

                    # self.optimalColSpeed_data.append(self.optimalColSpeed)
                    # self.optimalVerSpeed_data.append(self.optimalVerSpeed)
                    # self.optimalSpeed_data.append(self.optimalSpeed)

                    yield self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed
                    #一定要有这个生成器

    def func(self, generator):      #绘图函数
        # expand ax_x when t is larger than xlim
        # self.database = self.fobj.readlines()
        self.min, self.max = self.ax3.get_xlim()
        if self.t >= self.max:
            if self.t - self.max < 10:
                self.ax2.set_ylim(self.min + 10, self.max + 10)
                self.ax3.set_xlim(self.min + 10, self.max + 10)
                self.ax4.set_xlim(self.min + 10, self.max + 10)
                self.ax5.set_xlim(self.min + 10, self.max + 10)
                self.axFl.set_xlim(self.min + 10, self.max + 10)
                self.axFr.set_xlim(self.min + 10, self.max + 10)
                self.axBl.set_xlim(self.min + 10, self.max + 10)
                self.axBr.set_xlim(self.min + 10, self.max + 10)

                self.ax2.figure.canvas.draw()
                self.ax3.figure.canvas.draw()
                self.ax4.figure.canvas.draw()
                self.ax5.figure.canvas.draw()
                self.axFl.figure.canvas.draw()
                self.axFr.figure.canvas.draw()
                self.axBl.figure.canvas.draw()
                self.axBr.figure.canvas.draw()
            else:
                self.ax2.set_ylim(self.t//10*10, self.t//10*10 + 50)
                self.ax3.set_xlim(self.t//10*10, self.t//10*10 + 50)
                self.ax4.set_xlim(self.t//10*10, self.t//10*10 + 50)
                self.ax5.set_xlim(self.t//10*10, self.t//10*10 + 50)
                self.axFl.set_xlim(self.t//10*10, self.t//10*10 + 50)
                self.axFl.set_xlim(self.t//10*10, self.t//10*10 + 50)
                self.axBl.set_xlim(self.t//10*10, self.t//10*10 + 50)
                self.axBl.set_xlim(self.t//10*10, self.t//10*10 + 50)

                self.ax2.figure.canvas.draw()
                self.ax3.figure.canvas.draw()
                self.ax4.figure.canvas.draw()
                self.ax5.figure.canvas.draw()
                self.axFl.figure.canvas.draw()
                self.axFl.figure.canvas.draw()
                self.axBl.figure.canvas.draw()
                self.axBl.figure.canvas.draw()

        self.route.set_data(self.X_data, self.Y_data)
        self.angle.set_data(self.A_data, self.t_data)
        # self.speed_x.set_data(self.t_data, self.Speed_X_data)
        # self.speed_y.set_data(self.t_data, self.Speed_Y_data)
        # self.speed.set_data(self.t_data, self.Speed_data)
        self.fl.set_data(self.t_data, self.flRot)
        self.fr.set_data(self.t_data, self.frRot)
        self.bl.set_data(self.t_data, self.blRot)
        self.br.set_data(self.t_data, self.brRot)

        self.lowPassSpeed_x.set_data(self.t_data, self.optimalColSpeed_data)
        self.lowPassSpeed_y.set_data(self.t_data, self.optimalVerSpeed_data)
        self.lowPassSpeed.set_data(self.t_data, self.optimalSpeed_data)

        return (self.route, self.angle, self.lowPassSpeed_x,
                self.lowPassSpeed_y, self.lowPassSpeed, self.fl,
                self.fr, self.bl, self.br)

    def animationInit(self):
        try:
            self.draw = animation.FuncAnimation(self.fig, self.func, self.generator,
                                                init_func=self.init, blit=False, interval=0,
                                                repeat=False)
        except serial.SerialException:
            raise serial.SerialException
        self.draw._start()      #somehow in PyQt5 method _start() dosen't execute automaticly, so I have to start it manuly.

        #the class is class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, **kwargs)
        #and it will exicute func per interval(ms)  and #frames is func's arg!!!#

    def animationStop(self):
        self.draw._stop()


class GUIsetting(QtWidgets.QMainWindow):        #建立GUI设置类（以Qt5为基类）
    def __init__(self, parent=None):        #构造函数
        QtWidgets.QMainWindow.__init__(self)
        # self.splash = QtWidgets.QSplashScreen(QtGui.QPixmap(os.path.split(os.path.realpath(__file__))[0] + "/map.png")) #loading image!!
        # self.splash.show()
        QtWidgets.QToolTip.setFont(QtGui.QFont('Myriad Set'))       #set text-font
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setWindowTitle('Console')
        self.statusBar().showMessage('Good luck with adjusting!')

        self.menubar = self.menuBar()
        self.menubar.addSeparator()
        self.file_menu = self.menubar.addMenu('&File')
        self.file_menu.addAction('&SavePoint', self.saveroute,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&saveEncoder', self.saveEncoder,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_D)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.help_menu = self.menubar.addMenu('&Help')
        self.help_menu.addAction('About', self.aboutMessage)

        self.main_widget = QtWidgets.QWidget(self)

        self.closeSignal = Communicator()

        # self.extensionLayout = QtWidgets.QGridLayout()

        self.hBox1 = QtWidgets.QHBoxLayout()
        self.hBox1.addStretch(1)
        self.hBox2 = QtWidgets.QHBoxLayout()
        self.hBox2.addStretch(1)
        self.vBox = QtWidgets.QVBoxLayout(self.main_widget)
        self.vBox.addStretch(1)

        self.graph = Graph(width=20, height=15, dpi=80)
        self.canvas = FigureCanvasQTAgg(self.graph.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.vBox.addWidget(self.canvas)
        self.vBox.addWidget(self.toolbar)
        self.combo = QtWidgets.QComboBox(self)
        self.hBox1.addWidget(self.combo)

        self.serialButton = QtWidgets.QPushButton('Open', self)
        self.serialButton.setCheckable(True)
        self.serialButton.setToolTip('<b>click</b> to open/close a serial port.')
        self.serialButton.resize(self.serialButton.sizeHint())
        self.serialButton.clicked[bool].connect(self.serialOperation)

        # self.plotButton = QtWidgets.QPushButton('Start', self)
        # self.plotButton.setCheckable(True)
        # self.plotButton.setToolTip('<b>click</b> to start/stop plot.')
        # self.plotButton.resize(self.plotButton.sizeHint())
        # self.plotButton.clicked[bool].connect(self.graphFunc)

        self.menuButton = QtWidgets.QPushButton('Menu', self)
        self.menuButton.setToolTip('<b>click</b> to show/hide extension function.')
        self.menuButton.resize(self.serialButton.sizeHint())
        self.menuButton.clicked.connect(self.showMenu)

        self.recordButton = QtWidgets.QPushButton('Record', self)
        self.recordButton.setToolTip('<b>click</b> to record time node.')
        self.recordButton.resize(self.recordButton.sizeHint())
        self.recordButton.clicked.connect(self.timeNodeRecord)
        self.timeNode = []

        self.clearButton = QtWidgets.QPushButton('Clear', self)
        self.clearButton.clicked.connect(self.graphClear)
        self.clearButton.setToolTip('<b>click</b> to clear the Figure.')
        self.clearButton.resize(self.clearButton.sizeHint())

        self.hBox1.addWidget(self.serialButton)
        # self.hBox1.addWidget(self.plotButton)
        self.hBox1.addWidget(self.recordButton)
        self.hBox1.addWidget(self.clearButton)
        self.hBox2.addWidget(self.menuButton)
        self.vBox.addLayout(self.hBox2)
        self.vBox.addLayout(self.hBox1)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.plottingFlag = False
        self.plotedFlag = False
        self.savedFlag = False      #unnecessary, But for readabiliy added it.

        self.show()
        self.checkModel()
        # self.t = threading.Thread(target=self.checkModel())
        # self.t.setDaemon(True)
        # self.t.start()
        # self.splash.finish()

    def checkModel(self):
        self.graph.ser.getAvailablePort()
        for i in self.graph.ser.available_port:
            self.combo.addItem(i)
        self.port = str(self.combo.currentText())

    def fileQuit(self):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            if self.saveEnsure('Do you want to save data before exit?'):
                self.closeSignal.signal.emit()
                sys.exit()
            else:
                pass
        else:
            if self.actionEnsure('Are you sure want to quit?'):
                self.closeSignal.signal.emit()
                sys.exit()
            else:
                pass

    def aboutMessage(self):
        QtWidgets.QMessageBox.about(self, 'About',
                                    """©2016 XJTU Roboteam. All Rights Reserved. <br/>
This is a program for cart adjusting. function completing.""")

    def closeEvent(self, event):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            if self.saveEnsure('Do you want to save data before exit?'):
                self.closeSignal.signal.emit()
                event.accept()
            else:
                event.ignore()
        else:
            if self.actionEnsure('Are you sure want to quit?'):
                self.closeSignal.signal.emit()
                event.accept()
            else:
                event.ignore()

    def saveEnsure(self, message, title='Warning'):
        reply = QtWidgets.QMessageBox.warning(self,
                                              title,
                                              message,
                                              QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel,
                                              QtWidgets.QMessageBox.Save)

        if reply == QtWidgets.QMessageBox.Save:
            self.graphFunc()
            self.saveroute()
            return True
        elif reply == QtWidgets.QMessageBox.Discard:
            return True
        else:
            return False

    def actionEnsure(self, message, title='Warning'):
        reply = QtWidgets.QMessageBox.question(self,
                                               title,
                                               message,
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Yes)

        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def information(self, message, title='reminder'):
        QtWidgets.QMessageBox.information(self, title, message)

    def warning(self, message, title='Warning'):
        QtWidgets.QMessageBox.warning(self, title, message)

    def saveroute(self):
        if len(self.graph.timeNode) != 0:
            fname = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          'Save timeNode File',
                                                          'timeNode%s.txt' % time.ctime(),
                                                          "Text Files (*.txt)")
            try:
                with open(fname[0], 'w') as self.fobj:
                    self.fobj.write(self.graph.timeCount())
                    self.savedFlag = True
            except Exception:
                self.warning('failed to operation the file.')
                print(Exception)
        else:
            self.warning('no time node recorded.')
        #-----------------------------function below is for save point after plotting-----------------------------------------
        # if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
        #     fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.split(os.path.realpath(__file__))[0])
        #     try:
        #         with open(fname[0], 'w') as self.fobj:
        #             self.PointRoute = list(zip(self.graph.X_data, self.graph.Y_data, self.graph.A_data, self.graph.Speed_X_data, self.graph.Speed_Y_data, self.graph.Speed_data))
        #             for item in self.PointRoute:
        #                 self.fobj.write('("posture",' + str(item) + ')' + '\n')
        #             self.information('successful saved.')
        #             self.plotedFlag = False
        #             self.savedFlag = True
        #     except Exception:
        #         self.warning('failed to open the file.')
        # else:
        #     self.warning('No new data received!')
        #----------------------------------------------------------------------------------------------------------------------

    def saveEncoder(self):
        if len(self.graph.encoder1_data) != 0:
            fname = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          'Save encoder File',
                                                          os.path.split(os.path.realpath(__file__))[0],
                                                          "Text Files (*.txt)",
                                                          'Fmt_encoder%s' % time.ctime())
            try:
                with open(fname[0], 'w') as self.fobj:
                    self.encoderData = list(zip(self.graph.X_data,
                                                self.graph.Y_data,
                                                self.graph.A_data,
                                                self.graph.encoder1_data,
                                                self.graph.encoder2_data))
                    for item in self.encoderData:
                        self.fobj.write(str(item) + '\n')
                    self.information('successful saved.')
                    self.savedFlag = True
            except Exception:
                self.warning('failed to operation the file.')
                print(Exception)
        else:
            self.warning('no time Data recorded.')

    def serialOperation(self, pressed):
        # try:
        if pressed:
            if self.graph.ser.serialInit(self.port):
                self.statusBar().showMessage('successful opened serial port.')
                self.serialButton.setText('Close')

                self.plottingFlag = True
                self.plotedFlag = True
                self.graph.animationInit()
                self.statusBar().showMessage('plotting.')
            else:
                self.warning('serial open error, please check if the model plugged in.')
                self.serialButton.setChecked(False)
                # self.serialButton.setText('Open')
        else:
            self.plottingFlag = False
            self.graph.animationStop()
            self.statusBar().showMessage('stoped')

            self.graph.ser.serialClose()
            self.serialButton.setText('Open')
        # except Exception:
            # self.warning('serial open error, please check if the model plugged in.')

    def graphFunc(self, pressed):
        if pressed:
            if self.serInitFlag:
                self.plottingFlag = True
                self.plotedFlag = True
                self.graph.animationInit()
                self.statusBar().showMessage('plotting.')
                self.plotButton.setText('Stop')
            else:
                self.warning('Please open serial port first!')
                self.plotButton.setChecked(False)
        else:
            self.plottingFlag = False
            self.graph.animationStop()
            self.statusBar().showMessage('stoped')
            self.plotButton.setText('Start')

    def graphClear(self):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            if self.saveEnsure('Do you wish to save data before clear Figure?'):
                self.graph.clear()
                self.encoderData = []
                self.plottingFlag = False
                self.plotedFlag = False
                self.savedFlag = False
            else:
                pass
        else:
            if self.actionEnsure('Are you sure wish to clear Figure?'):
                self.graph.clear()
                self.encoderData = []

                self.plotedFlag = False
                self.savedFlag = False
            else:
                pass

    def timeNodeRecord(self):
        self.information(self.graph.timeCount(), "Timer")

    def showMenu(self):
        self.menu = Menu(self.graph.ser)
        self.menu.show()
        self.closeSignal = Communicator()
        self.closeSignal.signal.connect(self.menu.close)


class Communicator(QtCore.QObject):
    signal = QtCore.pyqtSignal()


class Menu(QtWidgets.QMainWindow):
    def __init__(self, serObj):
        QtWidgets.QMainWindow.__init__(self)

        QtWidgets.QToolTip.setFont(QtGui.QFont('Myriad Set'))       #set text-font
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.setWindowTitle('Menu')
        self.statusBar().showMessage('Good luck with adjusting!')
        self.setGeometry(500, 300, 500, 309)

        self.transport = serObj

        self.main_widget = QtWidgets.QWidget(self)
        self.extension = QtWidgets.QVBoxLayout(self.main_widget)
        self.extension.addStretch(1)
        self.funcButtonBar = QtWidgets.QHBoxLayout()
        self.funcButtonBar.addStretch(1)

        self.label = QtWidgets.QLabel(self)
        self.label.setFont(QtGui.QFont("Myriad Set", 45, QtGui.QFont.Bold))
        self.label.setText("This is it!")
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.goRouteButton = QtWidgets.QPushButton('go Route', self)
        self.goRouteButton.setToolTip('<b>click</b> to go route.')
        self.goRouteButton.resize(self.goRouteButton.sizeHint())
        self.goRouteButton.clicked.connect(self.goRoute)

        self.emergencyButton = QtWidgets.QPushButton('emergency Stop', self)
        self.emergencyButton.setToolTip('<b>click</b> to force it stop.')
        self.emergencyButton.resize(self.emergencyButton.sizeHint())
        self.emergencyButton.clicked.connect(self.emergencyStop)

        self.funcButtonBar.addWidget(self.goRouteButton)
        self.funcButtonBar.addWidget(self.emergencyButton)
        self.extension.addLayout(self.funcButtonBar)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.setStyleSheet("QLabel{text-align:center;}"
                           "QLabel{margin:auto;}")
        self.label.adjustSize()

        self.runningFlag = False

    def goRoute(self):
        try:
            if not self.runningFlag:
                self.transport.writeCmd("43")
                self.runningFlag = True
            else:
                raise Exception
        except Exception:
            pass

    def emergencyStop(self):
        try:
            self.transport.writeCmd("6")
        except Exception:
            pass


if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)
    aw = GUIsetting()
    sys.exit(qApp.exec_())


#----------------------journal-----------------------#
# problem:                                           #
#   1. Can't do it real-time.                        #
#   2. Can't stop automaticly.                       #
#   3. need to excicute two process manually.        #
#   4. ugly.                                         #
#                                                    #
#---------------------2016.1.31----------------------#

#----------------real-time solution------------------#
# A. put readline() method into generator(done)      #
# B. read as many lines as you can at a time         #
#----------------------------------------------------#

#----------------------journal-----------------------#
# problem:                                           #
#   1. Can't stop automaticly.                       #
#   2. Program will be block when no data send.      #
#   3. Ugly.                                         #
#   4. Need to run it using thread programming.      #
#                                                    #
#----------------------2016.2.1----------------------#

#----------------------journal-----------------------#
# update:                                            #
#   1. Embedded the plot into Qt5(used to be Tkinter)#
#   2. Woring on complete the function               #
#   3. Thread block problem still unhandled          #
#                                                    #
#---------------------2016.2.17----------------------#

#----------------------journal-----------------------#
# update:                                            #
#   1. After added timeout=0 arg into serial init th-#
#      e thread block problem finnal solved. but the #
#      program would still stuck after plotting began#
#   2. The problem above was because when no data re-#
#      ceived program stuck into a endless loop of m-#
#      ethod generatorself.                          #
#   3. working on completing function                #
#                                                    #
#---------------------2016.2.18----------------------#

#-----------------------journal----------------------#
# update:                                            #
#   1. Solved many problems which was mentioned above#
#                                                    #
# problem:                                           #
#   1. Clear function dosen't work correctly.        #
#                                                    #
# blueprint:                                         #
#   1. Now that we are able to use uart to transport #
#      data from PC to cart, which means that it is  #
#      possible control cart by PC. It'll including  #
#      these function:                               #
#      (1) use keyboard as a joystick                #
#      (2) replace keyborad and LCD's function       #
#      (3) make a full use of PC's performance to do #
#          some adjust work like PID adjustment      #
#      (4) more to think and discuss.                #
#                                                    #
#---------------------2016.3.15----------------------#

#-----------------------journal----------------------#
# update:
#   1. Since I know that uart can do I/O the same t- #
#      me(almost), developed the control function.   #
#   2. Now using Lowpass filtering to ajust speed fi-#
#      gure and had a great effect.                  #
#   3. Rewrite clear function, now it's good to use  #
#   4. Rewrite axis limits auto-reset function, now  #
#      it will not take a long time to reset bit by  #
#      bit.                                          #
#                                                    #
# problem:                                           #
#   1. But goRoute function can't work well since ma-#
#      in control program changed, now click goRoute #
#      button with what click EnmergencyStop button  #
#      to dirve the cart. Need to fix this.          #
#                                                    #
# blueprint:                                         #
#   1. To make this software more useful. use it at  #
#      an analyse tool to have a speed-up of our dear#
#      cart.                                         #
#                                                    #
#---------------------2016.4.2-----------------------#

#-----------------------journal----------------------#
# updata:                                            #
#   1. Add 4 plots for four wheel rotation.          #
#   2. completed save function(auto generate its     #
#      name)                                         #
#                                                    #
# blueprint:                                         #
#   Same as one above                                #
#                                                    #
#---------------------2016.4.12----------------------#

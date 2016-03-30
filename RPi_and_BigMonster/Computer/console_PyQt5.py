#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-16 16:36:30
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-03-30 02:11:53
import matplotlib       #绘图库
matplotlib.use('Qt5Agg')        #qt5接口声明
from PyQt5 import QtGui, QtCore, QtWidgets      #qt
import sys
import numpy as np
import matplotlib.pyplot as plt         #绘图模块
import matplotlib.animation as animation        #动画模块
import matplotlib.gridspec as gridspec          #分块模块
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT          #图接口以及工具库
# implement the default mpl key bindings
import serial       #串口模块
import os
import platform
import struct

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
        for i in range(10):
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
        return self.ser.readline()

    def writeCmd(self, string):
        string = eval(string)
        string = struct.pack("H", string)
        print(string)
        print(type(string))
        self.ser.write(string)


class Graph():
    def __init__(self, width=20, height=10, dpi=80, xmin=-14000, xmax=0, ymin=0, ymax=14000):
        self.ser = SerialCtl()
        self.serRead = b''
        self.t = 0
        # 对整个图进行分区2列x4行
        self.subs = gridspec.GridSpec(2, 4)
        self.fig = plt.Figure(  #facecolor = "black",
                          figsize=(width, height), dpi=dpi)        #设定图大小20英寸x10英寸
        # 对图进行分割
        self.ax1 = self.fig.add_subplot(self.subs[0:, 1:-1])
        self.ax2 = self.fig.add_subplot(self.subs[0, 0], projection='polar')
        self.ax3 = self.fig.add_subplot(self.subs[1, 0])
        self.ax4 = self.fig.add_subplot(self.subs[0, -1])
        self.ax5 = self.fig.add_subplot(self.subs[1, -1])
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
        # 初始化并设定各子图样式
        self.route, = self.ax1.plot([], [], 'g-', lw=2)     #lw is linewidth
        self.stdB_route, = self.ax1.plot([], [], 'b-', lw=2)
        self.stdR_route, = self.ax1.plot([], [], 'r-', lw=2)
        self.angle, = self.ax2.plot([], [], 'b-', lw=2)
        self.speed_x, = self.ax3.plot([], [], 'b-', lw=2)
        self.speed_y, = self.ax4.plot([], [], 'b-', lw=2)
        self.speed, = self.ax5. plot([], [], 'b-', lw=2)
        # 设定路径图长宽
        self.ax1.set_xlim(xmin, xmax)
        self.ax1.set_ylim(ymin, ymax)
        # 对各图数据初始化
        self.stdB_X_data, self.stdB_Y_data, self.stdR_X_data, self.stdR_Y_data, self.X_data, self.Y_data, self.A_data, self.Speed_X_data, self.Speed_Y_data, self.Speed_data, self.t_data = [], [], [], [], [], [], [], [], [], [], []
        self.encoder1_data, self.encoder2_data = [], []
        self.optimalX_data, self.optimalY_data = [], []
        self.timeNode = []
        # 设定各图实时数据位置
        # self.Angle_display = self.ax1.text(-13900, 13700, '')
        # self.Speed_X_display = self.ax3.text(250, 950, '')
        # self.Speed_Y_display = self.ax4.text(250, 950, '')
        # self.Speed_display = self.ax5.text(250, 950, '')
        # 打开文件
        with open(os.path.split(os.path.realpath(__file__))[0]+'/Fmt_RouteBlue.txt', 'r') as self.stdB_fobj:
            self.database = self.stdB_fobj.readlines()
        for item in self.database:
            self.info = tuple(eval(item))
            self.stdB_X, self.stdB_Y, self.stdB_A, self.stdB_Speed_X, self.stdB_Speed_Y, self.stdB_Speed = self.info
            self.stdB_X_data.append(self.stdB_X)
            self.stdB_Y_data.append(-self.stdB_Y)
        self.stdB_route.set_data(self.stdB_X_data, self.stdB_Y_data)

        for item in range(0, len(self.database)):
            self.stdR_X_data.append(-self.stdB_X_data[item]-14000)
            self.stdR_Y_data.append(self.stdB_Y_data[item])
        self.stdR_route.set_data(self.stdR_X_data, self.stdR_Y_data)
        # self.fobj = open(os.path.split(os.path.realpath(__file__))[0]+'/route4.txt', 'r')     #this function will get the dir where the script is

        self.ax2.set_ylim(0, 50)
        self.ax3.set_xlim(0, 50)
        self.ax3.set_ylim(-3000, 3000)
        self.ax4.set_xlim(0, 50)
        self.ax4.set_ylim(-3000, 3000)
        self.ax5.set_xlim(0, 50)
        self.ax5.set_ylim(0, 3000)

        self.fig.tight_layout()

        #Kalman Filter params
        self.optimalX = 0
        self.optimalY = 0
        self.covariance = 10
        self.paramP = np.cov(np.random.randn(1, len(self.stdR_X_data)))
        self.paramQ = np.cov(np.random.randn(1, len(self.stdR_X_data)))

    def calculator(self):
        if len(self.X_data) < 3:
            self.Speed_X = self.Speed_Y = self.Speed = 0
        elif self.t_data[-1] - self.t_data[-2] == 0:
            self.Speed_X = self.Speed_X_data[-1]
            self.Speed_Y = self.Speed_Y_data[-1]
            self.Speed = self.Speed_data[-1]
        else:
            self.Speed_X = (self.X_data[-1] - self.X_data[-2]) / (self.t_data[-1] - self.t_data[-2])
            self.Speed_Y = (self.Y_data[-1] - self.Y_data[-2]) / (self.t_data[-1] - self.t_data[-2])
            self.Speed = np.sqrt(self.Speed_X ** 2 + self.Speed_Y ** 2)

    def kalmanFilter(self):
        if len(self.X_data) < 2:
            self.predictX = self.optimalX
            self.predictY = self.optimalY
        else:
            self.predictX = self.optimalX + self.stdB_X_data[len(self.X_data)] - self.stdB_X_data[len(self.X_data) - 1]
            self.predictY = self.optimalY + self.stdB_Y_data[len(self.Y_data)] - self.stdB_Y_data[len(self.Y_data) - 1]
        self.covariance += self.paramQ
        Kg = self.covariance/(self.covariance + self.paramQ)
        self.optimalX = self.predictX + Kg * (self.X_data[-1] - self.predictX)
        self.optimalY = self.predictY + Kg * (self.Y_data[-1] - self.predictY)
        self.covariance = (1 - Kg)/self.covariance
        self.optimalX_data.append(self.optimalX)
        self.optimalY_data.append(self.optimalY)
        #协方差怎么算

    def timeCount(self):
        if len(self.timeNode) != 0:
            timeRecord = ""
            for i in range(len(self.timeNode)):
                if i == 0:
                    timeRecord += ("大车路径点记录：\n第%.1f秒大车启动\n" % (self.timeNode[i]))
                else:
                    timeRecord += ("第%d段路径用时%.1f秒\n" % (i, self.timeNode[i]-self.timeNode[i-1]))
            if len(self.timeNode) == 19:
                timeRecord += ("路径用时%.1f秒，寻杆用时%.1f秒\n总计用时%.1f秒" % (self.timeNode[17]-self.timeNode[0], self.timeNode[18]-self.timeNode[17], self.timeNode[18]-self.timeNode[0]))
            else:
                timeRecord += ("总计用时%.1f秒" % (self.timeNode[-1]-self.timeNode[0]))
        else:
            timeRecord = "no data in the record"
        return timeRecord

    def init(self):         # 动画初始化

        self.route.set_data([], [])
        self.angle.set_data([], [])
        self.speed_x.set_data([], [])
        self.speed_y.set_data([], [])
        self.speed.set_data([], [])

        # self.Angle_display.set_text('')
        # self.Speed_X_display.set_text('')
        # self.Speed_Y_display.set_text('')
        # self.Speed_display.set_text('')
        return self.stdR_route, self.stdB_route, self.route, self.angle, self.speed_x, self.speed_y, self.speed  #, self.Speed_X_display, self.Angle_display, self.Speed_Y_display, self.Speed_display

    def clear(self):
        self.X_data, self.Y_data, self.A_data, self.Speed_X_data, self.Speed_Y_data, self.Speed_data = [], [], [], [], [], []

    def generator(self):      # 数据迭代器
        while True:
            self.serRead = self.ser.readline()
            if self.serRead == b'':
                self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed = None, None, None, None, None, None
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
                    print(self.type)
                else:
                    self.X, self.Y, self.A, self.t = self.info[0], self.info[1], self.info[2], self.info[-2]
                    self.encoder1, self.encoder2 = self.info[3], self.info[4]
                    self.calculator()
                    # print(self.info)
                    self.t_data.append(self.t)
                    self.X_data.append(self.X)
                    self.Y_data.append(self.Y)
                    self.A_data.append(self.A)
                    self.encoder1_data.append(self.encoder1)
                    self.encoder2_data.append(self.encoder2)
                    self.Speed_X_data.append(self.Speed_X)
                    self.Speed_Y_data.append(self.Speed_Y)
                    self.Speed_data.append(self.Speed)
                    # self.Angle_display.set_text('Angle = %.2f' % (self.A))
                    # self.Speed_X_display.set_text('Speed_X = %.2f' % self.Speed_X)
                    # self.Speed_Y_display.set_text('Speed_Y = %.2f' % self.Speed_Y)
                    # self.Speed_display.set_text('Speed = %.2f' % self.Speed)
                    yield self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed
                    #一定要有这个生成器

    def func(self, generator):      #绘图函数
        # expand ax_x when t is larger than xlim
        # self.database = self.fobj.readlines()
        self.min, self.max = self.ax3.get_xlim()
        if self.t >= self.max:
            self.ax2.set_ylim(self.min + 10, self.max + 10)
            self.ax3.set_xlim(self.min + 10, self.max + 10)
            self.ax4.set_xlim(self.min + 10, self.max + 10)
            self.ax5.set_xlim(self.min + 10, self.max + 10)
            self.ax2.figure.canvas.draw()
            self.ax3.figure.canvas.draw()
            self.ax4.figure.canvas.draw()
            self.ax5.figure.canvas.draw()

        self.route.set_data(self.X_data, self.Y_data)
        self.angle.set_data(self.A_data, self.t_data)
        self.speed_x.set_data(self.t_data, self.Speed_X_data)
        self.speed_y.set_data(self.t_data, self.Speed_Y_data)
        self.speed.set_data(self.t_data, self.Speed_data)

        return self.route, self.angle, self.speed_x, self.speed_y, self.speed  #, self.Angle_display, self.Speed_X_display, self.Speed_Y_display, self.Speed_display

    def animationInit(self):
        self.draw = animation.FuncAnimation(self.fig, self.func, self.generator, init_func=self.init, blit=False, interval=0, repeat=False)
        self.draw._start()      #somehow in PyQt5 method _start() dosen't execute automaticly, so I have to start it manuly.

        #the class is class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, **kwargs)
        #and it will exicute func per interval(ms)  and #frames is func's arg!!!#

    def animationStop(self):
        self.draw._stop()


class GUIsetting(QtWidgets.QMainWindow):        #建立GUI设置类（以Qt5为基类）
    def __init__(self, parent=None):        #构造函数
        QtWidgets.QMainWindow.__init__(self)
        # self.splash = QtWidgets.QSplashScreen(QtGui.QPixmap(os.path.split(os.path.realpath(__file__))[0] + "/map.png"))
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

        self.graph = Graph(width=20, height=10, dpi=80)
        self.canvas = FigureCanvasQTAgg(self.graph.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.vBox.addWidget(self.canvas)
        self.vBox.addWidget(self.toolbar)
        self.combo = QtWidgets.QComboBox(self)
        self.hBox1.addWidget(self.combo)
        self.checkModel()

        self.serialButton = QtWidgets.QPushButton('Open', self)
        self.serialButton.setCheckable(True)
        self.serialButton.setToolTip('<b>click</b> to open/close a serial port.')
        self.serialButton.resize(self.serialButton.sizeHint())
        self.serialButton.clicked[bool].connect(self.serialOperation)

        self.plotButton = QtWidgets.QPushButton('Start', self)
        self.plotButton.setCheckable(True)
        self.plotButton.setToolTip('<b>click</b> to start/stop plot.')
        self.plotButton.resize(self.plotButton.sizeHint())
        self.plotButton.clicked[bool].connect(self.graphFunc)

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
        self.hBox1.addWidget(self.plotButton)
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
        self.serInitFlag = 0
        self.show()
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
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save timeNode File')
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
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save encoder File')
            try:
                with open(fname[0], 'w') as self.fobj:
                    self.encoderData = list(zip(self.graph.X_data, self.graph.Y_data, self.graph.A_data, self.graph.encoder1_data, self.graph.encoder2_data))
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
                self.serInitFlag = True
                self.statusBar().showMessage('successful opened serial port.')
                self.serialButton.setText('Close')
            else:
                self.warning('serial open error, please check if the model plugged in.')
                self.serialButton.setChecked(False)
                # self.serialButton.setText('Open')
        else:
            self.graph.ser.serialClose()
            self.serInitFlag = False
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
            if self.plottingFlag:
                self.graphStop()
            if self.saveEnsure('Do you wish to save data before clear Figure?'):
                self.graph.fig.clf()
                self.plottingFlag = False
                self.plotedFlag = False
                self.savedFlag = False
            else:
                pass
        else:
            if self.actionEnsure('Are you sure wish to clear Figure?'):
                del self.graph
                self.graph = Graph(width=20, height=10, dpi=80)
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
# updates:                                           #
#   1. Embedded the plot into Qt5(used to be Tkinter)#
#   2. Woring on complete the function               #
#   3. Thread block problem still unhandled          #
#                                                    #
#---------------------2016.2.17----------------------#

#----------------------journal-----------------------#
# updates:                                           #
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
# updates:                                           #
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

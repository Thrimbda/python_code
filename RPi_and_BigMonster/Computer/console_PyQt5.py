#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-16 16:36:30
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-02-20 17:56:44
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtGui, QtCore, QtWidgets
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
# implement the default mpl key bindings
import serial
import os
import platform


class Graph():
    def __init__(self, width=20, height=10, dpi=80, xmin=-14000, xmax=0, ymin=0, ymax=14000):

        self.serInitFlag = self.serialInit(0)
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
        self.std_route, = self.ax1.plot([], [], 'r-', lw=2)
        self.angle, = self.ax2.plot([], [], 'b-', lw=2)
        self.speed_x, = self.ax3.plot([], [], 'b-', lw=2)
        self.speed_y, = self.ax4.plot([], [], 'b-', lw=2)
        self.speed, = self.ax5. plot([], [], 'b-', lw=2)
        # 设定路径图长宽
        self.ax1.set_xlim(xmin, xmax)
        self.ax1.set_ylim(ymin, ymax)
        # 对各图数据初始化
        self.std_X_data, self.std_Y_data, self.X_data, self.Y_data, self.A_data, self.Speed_X_data, self.Speed_Y_data, self.Speed_data, self.t_data = [], [], [], [], [], [], [], [], []
        self.PointRoute = []
        # 设定各图实时数据位置
        # self.Angle_display = self.ax1.text(-13900, 13700, '')
        # self.Speed_X_display = self.ax3.text(250, 950, '')
        # self.Speed_Y_display = self.ax4.text(250, 950, '')
        # self.Speed_display = self.ax5.text(250, 950, '')
        # 打开文件
        with open(os.path.split(os.path.realpath(__file__))[0]+'/Fmt_PointRoute.txt', 'r') as self.std_fobj:
            self.database = self.std_fobj.readlines()[1:]
        for item in self.database:
            self.type, self.info = tuple(eval(item))
            self.std_X, self.std_Y, self.std_A, self.std_Speed_X, self.std_Speed_Y, self.std_Speed = self.info
            self.std_X_data.append(self.std_X)
            self.std_Y_data.append(self.std_Y)
        self.std_route.set_data(self.std_X_data, self.std_Y_data)
        # self.fobj = open(os.path.split(os.path.realpath(__file__))[0]+'/route4.txt', 'r')     #this function will get the dir where the script is

        self.ax2.set_ylim(0, 500)
        self.ax3.set_xlim(0, 500)
        self.ax3.set_ylim(-3000, 3000)
        self.ax4.set_xlim(0, 500)
        self.ax4.set_ylim(-3000, 3000)
        self.ax5.set_xlim(0, 500)
        self.ax5.set_ylim(0, 3000)

        self.available_port = []
        self.serRead = b''

        self.fig.tight_layout()

    def serialInit(self, portnum):
        try:
            if platform.system() == 'Linux':
                self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=0)
            elif platform.system() == 'Windows':
                self.ser = serial.Serial(portnum, baudrate=115200, timeout=0)
        except Exception:
            return False
        else:
            return True

    def getAvailablePort(self):
        for i in range(10):
            try:
                s = serial.Serial(i)
                self.available_port.append(i)
                s.close()
            except Exception:
                pass

    def calculator(self):
        if len(self.X_data) < 2:
            self.Speed_X = self.Speed_Y = self.Speed = 0
        else:
            self.Speed_X = (self.X_data[-1] - self.X_data[-2]) / (self.t_data[-1] - self.t_data[-2])
            self.Speed_Y = (self.Y_data[-1] - self.Y_data[-2]) / (self.t_data[-1] - self.t_data[-2])
            self.Speed = np.sqrt(self.Speed_X ** 2 + self.Speed_Y ** 2)

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
        return self.std_route, self.route, self.angle, self.speed_x, self.speed_y, self.speed  #, self.Speed_X_display, self.Angle_display, self.Speed_Y_display, self.Speed_display

    def generator(self):      # 数据迭代器
        while True:
            self.serRead = self.ser.readline()
            if self.serRead == b'':
                self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed = None, None, None, None, None, None
                yield self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed
                # this yield is very importent. without it the program will get into a endless loop here.
            else:
                try:
                    self.type, self.info = tuple(eval(self.serRead))
                except Exception:
                    self.type = 'bad_datatype'
                else:
                    if self.type == 'state':
                        self.AP, self.AI, self.AD, self.DP, self.DI, self.DD = self.info
                    # ,self.End_X, self.End_Y, self.SpdMx, self.AimA
                    if self.type == 'postrure':
                        self.X, self.Y, self.A, self.t = self.info

                        self.t_data.append(self.t)
                        self.X_data.append(self.X)
                        self.Y_data.append(self.Y)
                        self.A_data.append(self.A)
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
            self.ax2.set_ylim(self.min + 100, self.max + 100)
            self.ax3.set_xlim(self.min + 100, self.max + 100)
            self.ax4.set_xlim(self.min + 100, self.max + 100)
            self.ax5.set_xlim(self.min + 100, self.max + 100)
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
        if self.serInitFlag:
            self.draw = animation.FuncAnimation(self.fig, self.func, self.generator, init_func=self.init, blit=False, interval=0, repeat=False)
            self.draw._start()      #somehow in PyQt5 method _start() dosen't execute automaticly, so I have to start it manuly.
        else:
            print('Failed Init serial port.')

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
        # self.file_menu.addAction('&Real-time Plot', self.initgraph,
                                 # QtCore.Qt.CTRL + QtCore.Qt.Key_R)
        self.file_menu.addAction('&SavePoint', self.saveroute,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_S)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.help_menu = self.menubar.addMenu('&Help')
        self.help_menu.addAction('About', self.aboutMessage)

        self.main_widget = QtWidgets.QWidget(self)
        self.hBox = QtWidgets.QHBoxLayout()
        self.hBox.addStretch(1)
        self.vBox = QtWidgets.QVBoxLayout(self.main_widget)
        self.vBox.addStretch(1)

        self.graph = Graph(width=20, height=10, dpi=80)
        self.canvas = FigureCanvasQTAgg(self.graph.fig)
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.vBox.addWidget(self.canvas)
        self.vBox.addWidget(self.toolbar)

        self.combo = QtWidgets.QComboBox(self)
        for i in self.graph.available_port:
            self.combo.addItem("COM"+str(i))

        self.startButton = QtWidgets.QPushButton('Start', self)
        self.startButton.clicked.connect(self.graphInit)
        self.startButton.setToolTip('<b>click</b> to start plot.')
        self.startButton.resize(self.startButton.sizeHint())
        self.stopButton = QtWidgets.QPushButton('Stop', self)
        self.stopButton.clicked.connect(self.graphStop)
        self.stopButton.setToolTip('<b>click</b> to stop plot.')
        self.stopButton.resize(self.stopButton.sizeHint())
        self.clearButton = QtWidgets.QPushButton('Clear', self)
        self.clearButton.clicked.connect(self.graphClear)
        self.clearButton.setToolTip('<b>click</b> to clear the Figure.')
        self.clearButton.resize(self.clearButton.sizeHint())
        self.hBox.addWidget(self.combo)
        self.hBox.addWidget(self.startButton)
        self.hBox.addWidget(self.stopButton)
        self.hBox.addWidget(self.clearButton)
        self.vBox.addLayout(self.hBox)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.plottingFlag = False
        self.plotedFlag = False
        self.savedFlag = False      #unnecessary, But for readabiliy added it.
        self.show()
        # self.splash.finish()

    def fileQuit(self):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            if self.saveEnsure('Are you sure want to quit?'):
                sys.exit()
            else:
                pass
        else:
            sys.exit()

    def aboutMessage(self):
        QtWidgets.QMessageBox.about(self, 'About',
                                    """©2016 XJTU Roboteam. All Rights Reserved. <br/>
This is a program for cart adjusting. function completing.""")

    def closeEvent(self, event):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            if self.saveEnsure('Do you want to save data before exit?'):
                event.accept()
            else:
                event.ignore()
        else:
            if self.actionEnsure('Are you sure want to quit?'):
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
            self.graphStop()
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
                                               QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            return True
        else:
            return False

    def information(self, message, title='reminder'):
        QtWidgets.QMessageBox.information(self, title, message)

    def warning(self, message, title='Warning'):
        QtWidgets.QMessageBox.warning(self, title, message)

    def saveroute(self):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', os.path.split(os.path.realpath(__file__))[0])
            try:
                with open(fname[0], 'w') as self.fobj:
                    self.PointRoute = list(zip(self.graph.X_data, self.graph.Y_data, self.graph.A_data, self.graph.Speed_X_data, self.graph.Speed_Y_data, self.graph.Speed_data))
                    for item in self.PointRoute:
                        self.fobj.write('("posture",' + str(item) + ')' + '\n')
                    self.information('successful saved.')
                    self.plotedFlag = False
                    self.savedFlag = True
            except Exception:
                self.warning('failed to open the file.')
        else:
            self.warning('No new data received!')

    def graphInit(self):
        if not self.plottingFlag:
            if self.graph.serialInit():
                self.graph.serInitFlag = True
                self.plottingFlag = True
                self.plotedFlag = True
                self.graph.animationInit()
                self.statusBar().showMessage('plotting.')
            else:
                self.warning("Failed to open Serial Port. Please check your USB to TTL modle")
        else:
            self.warning("already started!")

    def graphStop(self):
        if self.plottingFlag:
            self.plottingFlag = False
            self.graph.animationStop()
            self.statusBar().showMessage('stoped')
        else:
            pass

    def graphClear(self):
        if (not self.savedFlag and self.plotedFlag) or self.plottingFlag:
            if self.saveEnsure('Do you wish to save data before clear Figure?'):
                self.graph.init()
                self.plottingFlag = False
                self.plotedFlag = False
                self.savedFlag = True
            else:
                pass
        else:
            if self.plottingFlag:
                self.graphStop()
            if self.actionEnsure('Are you sure wish to clear Figure?'):
                self.graph.init()
                self.plotedFlag = False
                self.savedFlag = True
            else:
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
#      program would still stuck after plotting began.#
#   2. The problem above was because when no data re-#
#      ceived program stuck into a endless loop of m-#
#      ethod generatorself.                          #
#   3. working on completing function                #
#                                                    #
#---------------------2016.2.18----------------------#

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-14 11:39:07
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-02-18 16:30:40
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import serial
import tkinter as tk
import os
import threading


class Graph():
    def __init__(self, xmin, xmax, ymin, ymax):

        self.ser = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout=1)
        self.t = 0
        self.fobj = open('/home/michael/Documents/python_code/RPi_and_BigMonster/Computer/PointRoute2.txt', 'w')
        # 对整个图进行分区2列x4行
        self.subs = gridspec.GridSpec(2, 4)
        self.fig = plt.Figure(  #facecolor = "black",
                          figsize=(20, 10))        #设定图大小20英寸x10英寸
        self.fig.tight_layout()
        # 对图进行分割
        self.ax1 = self.fig.add_subplot(self.subs[0:, 1:-1])
        self.ax2 = self.fig.add_subplot(self.subs[0, 0], projection='polar')
        self.ax3 = self.fig.add_subplot(self.subs[1, 0])
        self.ax4 = self.fig.add_subplot(self.subs[0, -1])
        self.ax5 = self.fig.add_subplot(self.subs[1, -1])
        # 设定各子图标题
        self.ax1.set_title("Cart's route")
        self.ax2.set_title("Angle")
        self.ax3.set_title("speed:X")
        self.ax4.set_title("speed:Y")
        self.ax5.set_title("speed:total")
        # 初始化并设定各子图样式
        self.route, = self.ax1.plot([], [], 'g-', lw=2)     #lw is linewidth
        self.std_route, = self.ax1.plot([], [], 'r-w', lw=2)
        self.angle, = self.ax2.plot([], [], 'b-', lw=2)
        self.speed_x, = self.ax3.plot([], [], 'b-', lw=2)
        self.speed_y, = self.ax4.plot([], [], 'b-', lw=2)
        self.speed, = self.ax5. plot([], [], 'b-', lw=2)
        # 设定路径图长宽
        self.ax1.set_xlim(xmin, xmax)
        self.ax1.set_ylim(ymin, ymax)
        # 对各图数据初始化
        self.std_X_data, self.std_Y_data, self.X_data, self.Y_data, self.A_data, self.Speed_X_data, self.Speed_Y_data, self.Speed_data, self.t_data = [], [], [], [], [], [], [], [], []
        self.t = 0
        self.PointRoute = []
        # 设定各图实时数据位置
        self.Angle_display = self.ax1.text(-13900, 13700, '')
        self.Speed_X_display = self.ax3.text(250, 950, '')
        self.Speed_Y_display = self.ax4.text(250, 950, '')
        self.Speed_display = self.ax5.text(250, 950, '')
        # 打开文件
        self.std_fobj = open(os.path.split(os.path.realpath(__file__))[0]+'/Fmt_PointRoute.txt', 'r')
        self.database = self.std_fobj.readlines()[1:]
        # self.fobj = open(os.path.split(os.path.realpath(__file__))[0]+'/route4.txt', 'r')     #this function will get the dir where the script is

        self.ax2.set_ylim(0, 500)
        self.ax3.set_xlim(0, 500)
        self.ax3.set_ylim(-3000, 3000)
        self.ax4.set_xlim(0, 500)
        self.ax4.set_ylim(-3000, 3000)
        self.ax5.set_xlim(0, 500)
        self.ax5.set_ylim(0, 3000)

    def saveRoute(self):
        self.PointRoute = list(zip(self.X_data, self.Y_data, self.A_data, self.Speed_X_data, self.Speed_Y_data, self.Speed_data))
        for item in self.PointRoute:
            self.fobj.write(self.PointRoute + '\n')

    def init(self):         # 动画初始化
        for item in self.database:
            self.type, self.info = tuple(eval(item))
            self.std_X, self.std_Y, self.std_A, self.std_Speed_X, self.std_Speed_Y, self.std_Speed = self.info
            self.std_X_data.append(self.std_X)
            self.std_Y_data.append(self.std_Y)
        self.std_route.set_data(self.std_X_data, self.std_Y_data)

        self.route.set_data([], [])
        self.angle.set_data([], [])
        self.speed_x.set_data([], [])
        self.speed_y.set_data([], [])
        self.speed.set_data([], [])

        self.Angle_display.set_text('')
        self.Speed_X_display.set_text('')
        self.Speed_Y_display.set_text('')
        self.Speed_display.set_text('')
        return self.std_route, self.route, self.angle, self.speed_x, self.Speed_X_display, self.speed_y, self.Angle_display, self.speed, self.Speed_Y_display, self.Speed_display

    def generator(self):      # 数据迭代器
        while True:
            self.t += 1
            try:
                self.type, self.info = tuple(eval(self.ser.readline()))
            except Exception:
                self.type = 'bad_datatype'
            else:
                if self.type == 'state':
                    self.AP, self.AI, self.AD, self.DP, self.DI, self.DD = self.info
                # ,self.End_X, self.End_Y, self.SpdMx, self.AimA
                if self.type == 'postrure':
                    self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed = self.info
                    self.t_data.append(self.t)
                    self.X_data.append(self.X)
                    self.Y_data.append(self.Y)
                    self.A_data.append(self.A)
                    self.Speed_X_data.append(self.Speed_X)
                    self.Speed_Y_data.append(self.Speed_Y)
                    self.Speed_data.append(self.Speed)
                    self.Angle_display.set_text('Angle = %.2f' % (self.A))
                    self.Speed_X_display.set_text('Speed_X = %.2f' % self.Speed_X)
                    self.Speed_Y_display.set_text('Speed_Y = %.2f' % self.Speed_Y)
                    self.Speed_display.set_text('Speed = %.2f' % self.Speed)
            # if frames == self.database[-1]:
                # input()
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

        return self.route, self.angle, self.speed_x, self.speed_y, self.speed, self.Angle_display, self.Speed_X_display, self.Speed_Y_display, self.Speed_display

    def drawAni(self):
        self.draw = animation.FuncAnimation(self.fig, self.func, self.generator, init_func=self.init, blit=True, interval=0, repeat=False)
        #the class is class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, **kwargs)
        #and it will exicute func per interval(ms)  and #frames is func's arg!!!#


class GUIsetting():        #建立GUI设置类（以网络适配器配置类为基类）
    def __init__(self, parent=None):        #构造函数
        self.top = tk.Frame(parent)        #设置父元素窗口
        self.top.pack()        #打包父元素
        self.graph = Graph(-14000, 0, 0, 14000)
        self.canvas = FigureCanvasTkAgg(self.graph.fig, self.top)
        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.top)
        self.make_widgets()        #调用配置函数Figure

    def make_widgets(self):     #配置函数
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        tk.Label(self.top, text='Cart console').pack(side=tk.TOP)       #介绍信息
        tk.Button(self.top, text='save PointRoute', command=self.saveroute).pack(side=tk.LEFT, fill=tk.BOTH, anchor=tk.W)      #设置查看当前ip按钮并定位
        tk.Button(self.top, text='Start', command=self.initgraph).pack(side=tk.LEFT)
        # tk.Button(self.top, text='close serial port', command=self.closeserport).pack(side=tk.LEFT)

    def saveroute(self):
        self.t1 = threading.Thread(target=self.graph.saveRoute)
        self.t1.start()

    def initgraph(self):
        self.t2 = threading.Thread(target=self.graph.drawAni)
        self.t2.daemon = True
        self.t2.start()


if __name__ == '__main__':
    figure = GUIsetting()
    figure.top.mainloop()


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

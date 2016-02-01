# receive the data from cart and draw its route by matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
# import serial
# from Recv_UDP import *

# class Communicata_ARM:			#receive data from ARM and send command to ARM
	# def __init__(self):
		# self.ser = serial.Serial('/dev/ttyUSB0', baudrate = 115200)
# 
	# def Readline(self):
		# self.string = self.ser.readline().decode()
		# return self.string

class graph():
    def __init__(self, xmin, xmax, ymin, ymax, IPaddress, Port, timeout):
        # Recv_UDP.__init__(self, IPaddress, Port, timeout)
        # 对整个图进行分区2列x4行
        self.subs = gridspec.GridSpec(2,4)
        self.fig = plt.figure(figsize = (20, 10))        #设定图大小20英寸x10英寸
        # 对图进行分割
        self.ax1 = self.fig.add_subplot(self.subs[0:, 1:-1])
        self.ax2 = self.fig.add_subplot(self.subs[0,0], projection='polar')
        self.ax3 = self.fig.add_subplot(self.subs[1,0])
        self.ax4 = self.fig.add_subplot(self.subs[0,-1])
        self.ax5 = self.fig.add_subplot(self.subs[1,-1])
        # 设定各子图标题
        self.ax1.set_title("Cart's route")
        self.ax2.set_title("Angle")
        self.ax3.set_title("speed:X")
        self.ax4.set_title("speed:Y")
        self.ax5.set_title("speed:total")
        # 初始化并设定各子图样式
        self.route,  = self.ax1.plot([], [], 'g-', lw = 2)		#lw is linewidth
        self.angle,  = self.ax2.plot([], [], 'b-', lw = 2)
        self.speed_x,  = self.ax3.plot([], [], 'b-', lw = 2)
        self.speed_y,  = self.ax4.plot([], [], 'b-', lw = 2)
        self.speed,  = self.ax5. plot([], [], 'b-', lw = 2)
        # 设定路径图长宽
        self.ax1.set_xlim(xmin, xmax)
        self.ax1.set_ylim(ymin, ymax)
        # 对各图数据初始化
        self.X_data, self.Y_data, self.A_data, self.Speed_X_data, self.Speed_Y_data, self.Speed_data, self.t_data = [], [], [], [], [], [], []
        # 设定各图实时数据位置
        self.Angle_display = self.ax1.text(-13900, 13700, '')
        self.Speed_X_display = self.ax3.text(250, 950, '')
        self.Speed_Y_display = self.ax4.text(250, 950, '')
        self.Speed_display = self.ax5.text(250, 950, '')
        # 打开测试用文件
        self.fobj = open('/home/michael/Documents/python_code/RPi_and_BigMonster/Computer/PointRoute.txt', 'r')
        self.type, self.state = tuple(eval(self.fobj.readline()))
        self.AP, self.AI, self.AD, self.DP, self.DI, self.DD = self.state
        # ,self.End_X, self.End_Y, self.SpdMx, self.AimA
        self.ax2.set_ylim(0, 1000)
        self.ax3.set_xlim(0, 1000)
        self.ax3.set_ylim(-2000, 2000)
        self.ax4.set_xlim(0, 1000)
        self.ax4.set_ylim(-2000, 2000)
        self.ax5.set_xlim(0, 1000)
        self.ax5.set_ylim(0, 2000)
        

    def init(self):			# 动画初始化
        self.route.set_data([], [])
        self.angle.set_data([], [])
        self.speed_x.set_data([], [])
        self.speed_y.set_data([], [])
        self.speed.set_data([], [])
        self.t = 0

        self.Angle_display.set_text('')
        self.Speed_X_display.set_text('')
        self.Speed_Y_display.set_text('')
        self.Speed_display.set_text('')
        return self.route, self.angle, self.speed_x, self.Speed_X_display, self.speed_y, self.Angle_display, self.speed, self.Speed_Y_display, self.Speed_display

    def generator(self):		# 数据迭代器
        self.database = self.fobj.readlines()[1:]
        for item in self.database:
            self.type, self.info = tuple(eval(item))
            if self.type == 'postrure':
                self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed = self.info
                self.A *=(np.pi/180)
                self.t_data.append(self.t)
                self.X_data.append(self.X)
                self.Y_data.append(self.Y)
                self.A_data.append(self.A)
                self.Speed_X_data.append(self.Speed_X)
                self.Speed_Y_data.append(self.Speed_Y)
                self.Speed_data.append(self.Speed)
                self.t += 1
                self.Angle_display.set_text('Angle = %.2f' % (self.A))
                self.Speed_X_display.set_text('Speed_X = %.2f' % self.Speed_X)
                self.Speed_Y_display.set_text('Speed_Y = %.2f' % self.Speed_Y)
                self.Speed_display.set_text('Speed = %.2f' % self.Speed)
            # if frames == self.database[-1]:
                # input()
            yield self.X, self.Y, self.A, self.Speed_X, self.Speed_Y, self.Speed   #一定要有这个生成器

    def func(self, generator):		#绘图函数
    # expand ax_x when t is larger than xlim
        self.min, self.max = self.ax3.get_xlim()
        if self.t >= self.max:
            self.ax2.set_ylim(self.min, 2*self.max)
            self.ax3.set_ylim(self.min, 2*self.max)
            self.ax4.set_ylim(self.min, 2*self.max)
            self.ax5.set_ylim(self.min, 2*self.max)
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
        self.draw = animation.FuncAnimation(self.fig, self.func, self.generator, init_func = self.init, blit = True, interval = 1)
        plt.show()
        #the class is class matplotlib.animation.FuncAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, **kwargs)
        #and it will exicute func per interval(ms)  and #frames is func's arg!!!#

if __name__ == '__main__':
    fig1 = graph(-14000, 0, -1000,14000, '192.168.10.90', 5005, 3)
    try:
        fig1.drawAni()
    finally:
        fig1.fobj.close()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Macpotty
# @Date:   2016-02-18 14:01:16
# @Last Modified by:   Macpotty
# @Last Modified time: 2016-02-18 14:04:09
# Edited by Macsnow 2015年10月12日20:04:37
# Hope you enjoy with it.
import wmi                                                                                                                                  #导入基于pywin32的wmi模块
from tkinter import *                                                                                                                       #导入tkinter模块用于建立图形界面
import sys                                                                                                                                  #导入sys模块


class SetNetWork:                                                                                                                           #建立网络适配器配置类
    def __init__(self):                                                                                                                     #构造函数
        self.objsettings = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)                                                        #命名objsettings为当前网关名
        self.objsetting = self.objsettings[0]
        self.aimIpAddress = ['192.168.10.90']                                                                                                 #设置IP地址变量
        self.aimSubnetMasks = ['255.255.255.0']                                                                                               #设置子网掩码变量
        self.aimDefaultGateways = ['192.168.10.1']                                                                                            #设置默认网关变量
        self.aimGatewayCostMetrics = [1]                                                                                                      #设置网关数量
        self.aimDNSServers = ['202.117.0.20', '202.117.0.21']                                                                                  #设置DNS服务器地址变量
        self.intReboot = 0                                                                                                                    #设置重启判断变量

    def SetIP(self):                                                                                                                        #设置IP函数
        return_value = self.objsetting.EnableStatic(IPAddress=self.aimIpAddress, SubnetMask=self.aimSubnetMasks)                               #更改IP地址并返回值（用以判断是否需要重启以生效）
        if return_value[0] == 0:                                                                                                              #若返回值为0，则修改成功且不需要重启
            print('成功设置IP')
        elif return_value[0] == 1:                                                                                                            #若返回值为1，则重启判断变量加1
            print('成功设置IP')
            self.intReboot += 1
        else:                                                                                                                               #否则未成功设置
            print('没有成功设置IP')
            sys.exit()

    def SetGateway(self):                                                                                                                   #设置网关函数
        return_value = self.objsetting.SetGateways(DefaultIPGateway=self.aimDefaultGateways, GatewayCostMetric=self.aimGatewayCostMetrics)     #更改默认网关并返回值（用以判断是否需要重启以生效）
        if return_value[0] == 0:                                                                                                              #若返回值为0，则修改成功且不需要重启
            print('成功设置网关')
        elif return_value[0] == 1:                                                                                                            #若返回值为1，则重启判断变量加1
            print('成功设置网关')
            self.intReboot += 1
        else:
            print('没有成功设置网关')                                                                                                           #否则未成功设置
            sys.exit()

    def SetDNS(self):                                                                                                                       ##设置DNS服务器函数
        return_value = self.objsetting.SetDNSServerSearchOrder(DNSServerSearchOrder=self.aimDNSServers)                                       #更改DNS服务器地址并返回值（用以判断是否需要重启以生效）
        if return_value[0] == 0:                                                                                                              #若返回值为0，则修改成功且不需要重启
            print('成功设置DNS')
        elif return_value[0] == 1:                                                                                                            #若返回值为1，则重启判断变量加1
            print('成功设置DNS')
            self.intReboot += 1
        else:                                                                                                                               #否则未成功设置
            print('没有成功设置DNS')
            sys.exit()


class GUIsetting(SetNetWork):                                                                                                               #建立GUI设置类（以网络适配器配置类为基类）
    def __init__(self, parent=None):                                                                                                         #构造函数
        SetNetWork.__init__(self)                                                                                                           #调用基类构造函数
        self.top = Frame(parent)                                                                                                              #设置父元素窗口
        self.top.pack()                                                                                                                     #打包父元素
        self.make_widgets()                                                                                                                 #调用配置函数

    def make_widgets(self):                                                                                                                 #配置函数
        Label(self.top, text='改ip小脚本 版本0.0.1').pack(side=LEFT, anchor=N)                                                                  #介绍信息
        Button(self.top, text='查看当前ip信息', command=self.massage).pack(side=BOTTOM, anchor=W)                                               #设置查看当前ip按钮并定位
        Button(self.top, text='更改为预设ip', command=self.settingIP).pack(side=BOTTOM, anchor=E)                                              #设置更改ip按钮并定位

    def settingIP(self):                                                                                                                    #更改ip按钮回调函数
        print('正在设置ip...')
        self.SetIP()                                                                                                                        #设置ip
        self.SetGateway()                                                                                                                   #设置网关
        self.SetDNS()                                                                                                                       #设置DNS服务器地址
        if self.intReboot > 0:                                                                                                                #检索重启判断变量值
            print('需要重启计算机以更新设置')
        else:
            SetNetWork.__init__(self)
            print('修改后的网络配置为：')                                                                                                     #输出更改后的网络配置
            print('IP: ', str(self.objsetting.IPAddress))                                                                                    #输出更改后的IP地址
            print('子网掩码:', str(self.objsetting.IPSubnet))                                                                                    #输出更改后子网掩码
            print('默认网关:', str(self.objsetting.DefaultIPGateway))                                                                            #输出更改后默认网关
            print('DNS:', str(self.objsetting.DNSServerSearchOrder))                                                                         #输出更改后DNS服务器

    def massage(self):                                                                                                                      #在当前网络适配器中循环
        if len(self.objsettings) < 1:                                                                                                         #判断如果网络适配器数量小于1
            print('没有找到可用的网络适配器')
            sys.exit()
        SetNetWork.__init__(self)
        for objsetting in self.objsettings:
            print(objsetting.Index)                                                                                                         #输出当前项index信息
            print(objsetting.SettingID)                                                                                                     #输出当前项网络ID
            print(objsetting.Description, objsetting.MACAddress)                                                                            #输出当前项网络名称
            print(objsetting.IPAddress)                                                                                                     #输出当前项IP地址
            print(objsetting.IPSubnet)                                                                                                      #输出当前项子网掩码
            print(objsetting.DefaultIPGateway)                                                                                              #输出当前项默认网关
            print(objsetting.DNSServerSearchOrder)                                                                                          #输出当前项DNS服务器地址

GUIsetting().top.mainloop()                                                                                                                 #调用mainloop函数使组件树显示在屏幕上

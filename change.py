#encoding:utf-8
import re									#引入re模块
import win32ui								#引入win32ui模块
dlg = win32ui.CreateFileDialog(1)			#新建窗口
dlg.SetOFNInitialDir('E:/python_code')		#设定初始窗口
dlg.DoModal()								#新建窗口
f1=dlg.GetPathName()						#获取文件路径以及文件名
def removeBom(nfile):
    '''移除UTF-8文件的BOM字节'''
    BOM = b'\xef\xbb\xbf'
    existBom = lambda s: True if s==BOM else False
    f = open(nfile, 'rb')
    if existBom( f.read(3) ):
        fbody = f.read()
        #f.close()
        with open(nfile, 'wb') as f:
            f.write(fbody)
removeBom(f1)
try:										#使用try预计测试语句
	fr=open(f1,'r',encoding="utf-8")						#打开原文件
except:										#如果未打开窗口则输出错误信息
	print("错误：未打开任何文件")			#打印错误信息
else:										#如果窗口正常打开则执行后续语句
	f2='E:/python_3.5.0/newfile.html'		#新文件将创建在程序子目录
	fw=open(f2,'w')						#创建新文件
	line=fr.readline()						#读取文件第一行字符进入字符串line
	type(line)
	print(line)
	while line:								#循环
		p=re.compile(r'href=".*?"')			#利用正则表达式查找链接
		line=p.sub(r'href="#"',line)		#将找到的链接替换为无效链接
		fw.write(line.encode('unicode-escape').decode('utf-8'))	#将替换后的链接
		line=fr.readline()					#读取下一行
	fw.close()								#关闭新文件
finally:
	fr.close()								#关闭原文件

#很遗憾，这段代码在python2.7.10上可以正常运行，但是更新python3.5.0之后在第14行会有错误提示：
#UnicodeDecodeError: 'gbk' codec can't decode byte 0xbf in position 2: illegal multibyte sequence
#相信在未来的某天这个问题终将得到解决。

#更新：在经历一个多小时的资料查询之后发现是由于utf-8中有一个with Bom模式
#而网上下载的源码正是这个格式的Unicode编码，因此将其转变为without Bom即可 2015年9月24日22:33:46

#更新：后来再次调试发现问题除了Bom格式意外还有中文问题
#若文档为纯英文文档则程序顺利运行，而若其中有中文则依然出现UnicodeDecodError 2015年9月25日02:25:27

#更新：在open函数中加入encodin='utf-8'参数后readline方法变为可用，此时若使用print方法则稳当全部正确显示
#但是write方法依然存在编码问题加入这句fw.write(line.encode('unicode-escape').decode('utf-8'))后勉强得到解决
#但是所有中文都显示不出2015年10月4日15:18:56
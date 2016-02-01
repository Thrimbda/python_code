class adder:
	def __init__(self,first=[]):
		self.data=first
	def add(self,x,y):
		print 'Not Impelmented'
	def __add__(self,other):
		return self.add(self.data,other)
	def __radd__(self,other):
		return self.add(other,self.data)
class listadder(adder):
	def add(self,x,y):
		return x+y
class dictadder(adder):
	def add(self,x,y):
		new={}
		new.update(x)
		new.update(y)
		return new
class Mylist:
	def __init__(self,value=[]):
		self.data=value
	def __add__(self,value):
		return Mylist(self.data+value)
	def __radd__(self,value):
		return Mylist(value+self.data)
	def __iadd__(self,value):
		return Mylist(self.data+value)
	def __mul__(self,value):
		return Mylist(self.data*value)
	def __getitem__(self,value):
		return self.data[value]
	def __len__(self,value):
		return len(self.data)
	def __getslice__(self,a,b):
		return Mylist(self.data[a:b])
	def append(self,value):
		return self.data.append(value)
	def __getattr__(self,name):
		return getattr(self.data,name)
	def __repr__(self):
		return repr(self.data)

class MylistSub(Mylist):
	calls=0
	def __init__(self,value=[]):
		self.adds=0
		Mylist.__init__(self,value)
	def __add__(self,value):
		MylistSub.calls+=1
		self.adds+=1
		return Mylist.__add__(self,value)
	def stats(self):
		return self.calls,self.adds
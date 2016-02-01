class Lunch:
	def __init__(self):
		self.Cust=Customer()
		self.Empl=Employee()
	def order(self,foodname):
		self.Cust.placeOrder(foodname,self.Empl)
	def result(self):
		self.Cust.printFood()
class Customer:
	def __init__(self):
		self.food=None
	def placeOrder(self,foodname,employee):
		self.food=Employee.takeOrder(employee,foodname)
	def printFood(self):
		print self.food.data
class Employee:
	def takeOrder(self,foodname):
		return Food(foodname)
class Food:
	def __init__(self,foodname):
		self.data=foodname
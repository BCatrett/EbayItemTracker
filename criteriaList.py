

class criteria(object):
	
	def __init__(self,userQuery,pricePoint,iList,eList):
		self.query=userQuery
		self.price=pricePoint
		self.includeList=iList
		self.excludeList=eList
	
	def displayCriteria(self):
		print(self.query)
		print(self.price)
		print(self.includeList)
		print(self.excludeList)
		
	def getQuery(self):
		return self.query
	
	def getPrice(self):
		return self.price
	
	def getIncludeList(self):
		return self.includeList
	
	def getExcludeList(self):
		return self.excludeList
		
def getCriteriaObject():
	
	query = input("Enter your search:")
	price = input("Enter your price:")
	iList=input("Enter the words you are looking for:")
	eList=input("Enter the words you want excluded:")
	return criteria(query,price,iList,eList)


from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import datetime
from datetime import timezone
from criteriaList import*
from GUIhed import *
import os, time, pytz
from threading import Thread
import re


utc = pytz.utc
pacific=pytz.timezone('US/Pacific')
now = datetime.datetime.now(pacific)

#retuns the price container of our CURRENT container
def getPrice(current):
	return (current.findAll("div", {"s-item__detail s-item__detail--primary"}))

#returns the date continer of our CURRECNT container
def getDate(current):
	return (current.findAll("span", {"s-item__detail s-item__detail--secondary"}))


	
#removes $ and commas from price, returns it as a float.
def formatPrice(price):
	formattedPrice=price.replace("$","").replace(",","")
	#there are some instnaces where the price is not defined in such a way 
	#it can be converted to a float, catch the error and set the price to a high, basically skipping over it
	try:
		formattedPrice=float(formattedPrice)
	except:
		formattedPrice=777777.77
		
	return formattedPrice
	
#formats day (removes spaces) so it is MMM-dd only
def formatDay(dateCont):
	return ((dateCont[0].text))

#converts title,include key words and exclude keywords into uppercase,repalces 
#commas with spaces then split into a list by spaces.
def formatElementOfTitleText(listIn):
	formattedList=listIn.upper()
	formattedList=formattedList.replace(","," ")
	formattedList=formattedList.split()
	return formattedList
		
def isAnElementOfTitle(title,objectList):
	
	#formats title,include keywords and exclude keywords
	thisIncludeList=formatElementOfTitleText(objectList.getIncludeList())
	#formats ebay title to remove special characters that prevent include/exclude matches
	#not included in formatElementOfTitleText because that method is used for multiple string conversions
	title=re.sub('[*!@~?\/)(|.,<>$%^&+-]',' ',title)
	
	titleList=formatElementOfTitleText(title)
	thisExcludeList=formatElementOfTitleText(objectList.getExcludeList())
	
	#checks if there is an exclude word present. If so, skip this item
	for eItem in thisExcludeList:
		if eItem in titleList:
			return False
			
	#checks if our include list is empty. If it is, we look at the entire title.		
	if len(thisIncludeList)==0:
		return True
		
	#checks if any include words are present in the title	
	for item in thisIncludeList:
		if item in titleList:
			return True
			
	return False


def setPageThreads(searchList):
	pageList=[]
	for items in searchList:
		pagesoupdProcess = Thread(target=setPage, args=[items])
		pagesoupdProcess.start()
		pageList.append(pagesoupdProcess)
		#time.sleep(5)
	
	for processes in pageList:
		pagesoupdProcess.join()
	
	return pageList
#reads the html file so it can be parsed
def setPage(searchList):
	
	#search=searchList
	catSearch=searchList.replace(" " , "+")
	my_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw="+catSearch+"&_sacat=0&LH_TitleDesc=0&_sop=10&rt=nc&LH_BIN=1"

	uClient = urlopen(my_url)
	pageHtml = uClient.read();
	uClient.close()
	pageSoup = soup(pageHtml, "html.parser")

	return pageSoup

	
def timeCriteriaIsMet(auctionListTime,executionInterval):
	listTimeObj=now.strptime('2019'+' '+auctionListTime,'%Y %b-%d %H:%M')
	
	#gets current time and saves it as an object for comparing
	currentTime=now.strftime("%Y %b-%d %H:%M")
	curTimeObj=now.strptime(currentTime,"%Y %b-%d %H:%M")
	
	#converts out time interval that is entered by user and sets it to a 
	#timedelta to compare against our time difference
	exeIntervalObj=datetime.timedelta(0,(executionInterval*60))
	
	if  (curTimeObj-listTimeObj) < exeIntervalObj:
			return True
	
	return False
	
def priceCriteriaIsMet(price,priceCriteria):
	
	if price<float(priceCriteria):
		return True
	return False
	
#display list in commandline	
def displayEntireList(objectList):
	for objects in objectList:
		objects.displayCriteria()

#returns a criteria object		
def getCriteriaObj(search,price,include,exclude):
	return criteria(search,price,include,exclude)

#attempts to save the current criteriaList. If we encounter an error return false(fail) otherwise success
def saveCriteriaList(list,fileName):
	try:
		file=open(fileName,"w")
	except Exception as e:
		print(e)
		return False
	#writes the list to a file seperated by '~'. This is the seperator used for reading.
	for items in list:
		line=(items.query +"~"+ items.price +"~"+ items.includeList +"~"+ items.excludeList +"\n")
		file.writelines(line)
	file.close()	
	return True

#loads a previous list of search criteria. Overwrites any previous information that is loaded/stored
#each element is seperated by ~
def readFile(thisFile,list):
	list.clear()
	tempList={}
	#i=0
	try:
		with open(thisFile,"r") as file:
			for line in file:
				tempList=line.split("~")
				list.append(getCriteriaObj(tempList[0],tempList[1],tempList[2],tempList[3]))
				print("tesssssssssssssssssssst")
				#i=i+1
		file.close()
	except:
		return False
	
	return True
#runs through all the searches entered by the user
def runSearch(list):
	threads=[]
	#reimplemented this with threads, the improvment was underwhelming
	#will refactor to thread the opening of the html pages and storing the data
	for items in list:
		process = Thread(target=searchEbay, args=[items])
		process.start()
		threads.append(process)
		#time.sleep(5)
	
	for processes in threads:
		process.join()
#Runs the ebay searches. 
def searchEbay(searchList):
	#load page into pagesoup
	
	pageSoup=setPage(searchList.getQuery())
	
	#establish container that stores price and date
	container=(pageSoup.findAll("div", {"class": "s-item__info clearfix"}))
	
	#establish container that stores a CLEAN title
	title2=(pageSoup.findAll("img", {"class": "s-item__image-img"}))
	
	i=0
	for con in container:
		current=con
		
		#grabs our title
		title3=(title2[i]["alt"])
		
		# grabs the price container that is in our CURRENT container and sets it to text
		priceCont=getPrice(current)
		price=(priceCont[0].text)
		price=formatPrice(price)
		
		#grabs the date container in our CURRENT container, sets it to text and splits it
		dateCont=getDate(current)
		
		#date=(dateCont[0].text).split()
		
		####OLD title. This uses  the price and date container. Refactored because this includes "New Listings" in the title. 
		#title=(current.a.h3.text)
		
		#formats our current container day
		day=formatDay(dateCont)
		
		#datetimeTEST=now.strptime('2019'+' '+day,'%Y %b-%d %H:%M')
		timeIsMet=timeCriteriaIsMet(day,4320)
		priceIsMet=priceCriteriaIsMet(price,searchList.getPrice())
		
		#check if any our criteria is met
		# if timeIsMet is not true then no other auctions on this page are true so we break
		if timeIsMet is True:
			if priceIsMet is True and isAnElementOfTitle(title3,searchList) is True:
				print(title3 + " " + str(price) + " " + day)
		else:
			break

		i=i+1
	


def main():
	
	
	criteriaList=[]
	App()
	

		
	
	print("END")
if __name__=="__main__":
	main()

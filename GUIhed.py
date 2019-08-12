import sys
from newItemTracker import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *



app = QApplication(sys.argv)


	
class App(QScrollArea,QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'Ebay Item Watch'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()
		
		sys.exit(app.exec_())
		
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.move(300,300)
		
		#define a list for our criteriaList objects
		critList=[]
		
		#create and add our ADDBUTTON to the main window. 
		#calls addCriteria to add new items to our critList list
		addSearchBtn = QPushButton("Add",self)
		addSearchBtn.resize(addSearchBtn.sizeHint())
		addSearchBtn.move(50,25)
		addSearchBtn.clicked.connect(lambda: self.addCriteria(critList))
		
		#create and add out DISPLAYLIST to the main window
		#calls displayCriteriaList which shows all elements of the critList list
		displayBtn = QPushButton("Display All Searches",self)
		displayBtn.resize(displayBtn.sizeHint())
		displayBtn.move(50,50)
		displayBtn.clicked.connect(lambda: self.displayCriteriaList(critList))
		
		saveListBtn = QPushButton("Save File",self)
		saveListBtn.resize(saveListBtn.sizeHint())
		saveListBtn.move(50,75)
		saveListBtn.clicked.connect(lambda:self.saveCritList(critList,1))
		
		saveNewListBtn = QPushButton("Save New File",self)
		saveNewListBtn.resize(saveNewListBtn.sizeHint())
		saveNewListBtn.move(50,100)
		saveNewListBtn.clicked.connect(lambda:self.saveCritList(critList,0))
		
		loadFileBtn = QPushButton("Load File",self)
		loadFileBtn.resize(loadFileBtn.sizeHint())
		loadFileBtn.move(50,125)
		loadFileBtn.clicked.connect(lambda:self.loadFile(critList))
		
		runBtn = QPushButton("Run",self)
		runBtn.resize(saveNewListBtn.sizeHint())
		runBtn.move(50,150)
		runBtn.clicked.connect(lambda:self.executeSearchDialogBox(critList))
		
		
		self.show()
		

	def addCriteria(self,list):
		
		#method to exctue our save button
		#pulls the text from the text boxes and then appends critList(passed as list) with this data
		#which adds the new criteriaList object by calling getCriteriaObj from newItemTrack.py
		def saveBtnClick():
			search=self.acWindow.searchTBox.text()
			price=self.acWindow.priceTBox.text()
			include=self.acWindow.includeTBox.text()
			exclude=self.acWindow.excludeTBox.text()
			list.append(getCriteriaObj(search,price,include,exclude))
			self.acWindow.close()
		
		#sets up the addCriteria window	
		self.acWindow = QDialog()
		self.acWindow.resize(940, 300)
		self.acWindow.move(300, 300)
		self.acWindow.setWindowTitle('Search Criteria Add/Edit')
		
		self.acWindow.horizontalGroupBox = QGroupBox("Search Criteria")
		self.acWindow.layout = QGridLayout()
		self.acWindow.layout.setColumnStretch(1, 4)
		#self.w.layout.setColumnStretch(2, 4)
        
		#define the text boxes for search,price,include and exclude
		self.acWindow.searchTBox = QLineEdit(self)
		self.acWindow.priceTBox = QLineEdit(self)
		self.acWindow.includeTBox = QLineEdit(self)
		self.acWindow.excludeTBox = QLineEdit(self)
		
		#define out search button which calls saveBtnClick 
		saveSearchBtn = QPushButton("Save",self.acWindow)
		saveSearchBtn.clicked.connect(lambda: saveBtnClick())
		
		#Add all of our labels and textboxes to the addCriteria (aCriteria) window
		self.acWindow.layout.addWidget(QLabel("Ebay Search"),0,0)
		self.acWindow.layout.addWidget(self.acWindow.searchTBox,0,1)
		
		self.acWindow.layout.addWidget(QLabel("Price:"),0,2)
		self.acWindow.layout.addWidget(self.acWindow.priceTBox,0,3)
		
		self.acWindow.layout.addWidget(QLabel("Include Words:"),2,0)
		self.acWindow.layout.addWidget(self.acWindow.includeTBox,2,1)
		
		self.acWindow.layout.addWidget(QLabel("Exclude Words"),3,0)
		self.acWindow.layout.addWidget(self.acWindow.excludeTBox,3,1)
		
		self.acWindow.layout.addWidget(saveSearchBtn,4,0)
		
		#set layout to acWindow
		self.acWindow.horizontalGroupBox.setLayout(self.acWindow.layout)
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.acWindow.horizontalGroupBox)
		self.acWindow.setLayout(windowLayout)
		
		self.acWindow.show()
			
		
		
	def displayCriteriaList(self,list):
	
		#set up QDialog box to display results
		self.DCL = QDialog()
		self.DCL.resize(940, 300)
		self.DCL.move(300, 300)
		self.DCL.setWindowTitle('Display All')
		
		
		
		
		self.DCL.horizontalGroupBox = QGroupBox("All Search Criteria")
		self.DCL.layout = QGridLayout()
		#self.w.layout.setColumnStretch(1, 4)
		#self.w.layout.setColumnStretch(2, 4)
        
		self.DCL.layout.addWidget(QLabel("Search Query"),0,0)
		self.DCL.layout.addWidget(QLabel("Price"),0,1)
		self.DCL.layout.addWidget(QLabel("Mandatory Words"),0,2)
		self.DCL.layout.addWidget(QLabel("Excluded Words"),0,3)
		
		
		
		#Loop that places all elements of our criteriaList(passed as list)
		#Also places Edit buttons -> calls editCriteriaList
		#Also places Delete Buttons -> calls deleteCriteriaEntry
		
		#define Edit and delete button lists
		EditBtn={}
		deleteBtn={}
		
		i=0
		
		for items in list:

			self.DCL.layout.addWidget(QLabel(items.query),i+1,0)
			self.DCL.layout.addWidget(QLabel(items.price),i+1,1)
			self.DCL.layout.addWidget(QLabel(items.includeList),i+1,2)
			self.DCL.layout.addWidget(QLabel(items.excludeList),i+1,3)
			
			EditBtn[i]=QPushButton("Edit"+str(i),self.DCL)
			deleteBtn[i]=QPushButton("Delete"+str(i),self.DCL)
			self.DCL.layout.addWidget(EditBtn[i],i+1,4)
			self.DCL.layout.addWidget(deleteBtn[i],i+1,5)
			EditBtn[i].clicked.connect(lambda throw_away=0, i=i: (self.DCL.close(), self.editCriteria(list[i],list)))
			deleteBtn[i].clicked.connect(lambda throw_away=0, i=i: (self.DCL.close(), self.deleteCriteriaEntry(int(i),list)))
			i=i+1
		
		#This is for formatting only: prints up to 30 lines to group the display window.
		z=i
		for z in range(1,30-z):
			self.DCL.layout.addWidget(QLabel("  "),z,0)
			z=z+1
		
		#applies the layout to our window
		self.DCL.horizontalGroupBox.setLayout(self.DCL.layout)
		
		windowLayout = QVBoxLayout()
	
		windowLayout.addWidget(self.DCL.horizontalGroupBox)
		self.DCL.setLayout(windowLayout)
		self.DCL.show()
	
	def editCriteria(self,list,fullList):
		
		#Save Button: grabs the text in the text boxes and updates the current list item(list)
		#Closes the window and re-displays the entire UPDATED list
		def saveBtnClick():
			list.query=self.EC.searchTBox.text()
			list.price=self.EC.priceTBox.text()
			list.includeList=self.EC.includeTBox.text()
			list.excludeList=self.EC.excludeTBox.text()
			#redisplay full list, close edit Window.
			self.displayCriteriaList(fullList)
			self.EC.close()
			
		#sets up a dialog box to edit the list item that was passed (list)	
		self.EC = QDialog()
		self.EC.resize(940, 300)
		self.EC.move(300, 300)
		self.EC.setWindowTitle('Search Criteria Add/Edit')
		
		self.EC.horizontalGroupBox = QGroupBox("Search Criteria")
		self.EC.layout = QGridLayout()
		self.EC.layout.setColumnStretch(1, 4)
		#self.EC.layout.setColumnStretch(2, 4)
        
		#define Search/Query textbox prefilled with the query for passed list item
		self.EC.searchTBox = QLineEdit(self)
		self.EC.searchTBox.setText(list.query)
		
		#define price textbox prefilled with the query for passed list item
		self.EC.priceTBox = QLineEdit(self)
		self.EC.priceTBox.setText(list.price)
		
		#define include textbox prefilled with the query for passed list item
		self.EC.includeTBox = QLineEdit(self)
		self.EC.includeTBox.setText(list.includeList)
		
		#define exclude textbox prefilled with the query for passed list item
		self.EC.excludeTBox = QLineEdit(self)
		self.EC.excludeTBox.setText(list.excludeList)
		
		#save button, runs saveBtnClick which stores the new values in the list index passed
		saveSearchBtn = QPushButton("Save",self.EC)
		saveSearchBtn.clicked.connect(lambda: saveBtnClick())
		
		#places the text labels for Search,price,Include words and Exclude Words
		self.EC.layout.addWidget(QLabel("Ebay Search"),0,0)
		self.EC.layout.addWidget(self.EC.searchTBox,0,1)
		
		self.EC.layout.addWidget(QLabel("Price:"),0,2)
		self.EC.layout.addWidget(self.EC.priceTBox,0,3)
		
		self.EC.layout.addWidget(QLabel("Include Words:"),2,0)
		self.EC.layout.addWidget(self.EC.includeTBox,2,1)
		
		self.EC.layout.addWidget(QLabel("Exclude Words"),3,0)
		self.EC.layout.addWidget(self.EC.excludeTBox,3,1)
		
		#add save button
		self.EC.layout.addWidget(saveSearchBtn,4,0)
		
		#places our layouts on EC Dialogue box
		self.EC.horizontalGroupBox.setLayout(self.EC.layout)
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.EC.horizontalGroupBox)
		self.EC.setLayout(windowLayout)
		
		self.EC.show()
		
	# passes criteriaList and deletes the index. Calls the updated displayCriteriaList
	def deleteCriteriaEntry(self,index,fullList):
		del(fullList[index])
		self.displayCriteriaList(fullList)
	
	#saves the users information, selection parameter determines if it is save as or save new
	def saveCritList(self,list,selection):
		if selection == 1:
			fileName=QFileDialog.getOpenFileName()
		else:
			fileName=QFileDialog.getSaveFileName()
		
		#call saveCriteriaList: displays a message if it is successful or not
		
		if(saveCriteriaList(list,fileName[0])):
			self.displayMessage("Save Successful!")
		else:
			self.displayMessage("Save Failed")
	
	def loadFile(self,list):
		fileName=QFileDialog.getOpenFileName()
		print(fileName)
		#call readFile: displays a message if it is successful or not
		test=readFile(fileName[0],list)
		print(test)
		if(test):
			self.displayMessage("Load Successful!")
		else:
			self.displayMessage("Load Failed")
		
	def executeSearchDialogBox(self,list):
		self.running = QDialog()
		self.running.resize(400, 200)
		self.running.move(300, 300)
		self.running.setWindowTitle('Running')
		
		self.running.horizontalGroupBox = QGroupBox("Running:")
		self.running.layout = QGridLayout()
		
		
		self.running.layout.addWidget(QLabel(""))
		
		self.running.horizontalGroupBox.setLayout(self.running.layout)
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.running.horizontalGroupBox)
		self.running.setLayout(windowLayout)
		
		executeBtn = QPushButton("Execute",self.running)
		self.running.layout.addWidget(executeBtn)
		executeBtn.resize(executeBtn.sizeHint())
		
		terminateBtn = QPushButton("Terminate",self.running)
		self.running.layout.addWidget(terminateBtn)
		executeBtn.resize(terminateBtn.sizeHint())
		#executeBtn.move(50,150)
		executeBtn.clicked.connect(lambda:self.executeSearch(list))
		
		self.running.show()	

		
	def executeSearch(self,searchList):
		
		runSearch(searchList)
		
		
	#dialogue box to show a message.
	def displayMessage(self,messageToDisplay):
		self.dMessage = QDialog()
		self.dMessage.resize(400, 200)
		self.dMessage.move(300, 300)
		self.dMessage.setWindowTitle('Message')
		
		self.dMessage.horizontalGroupBox = QGroupBox("Attention:")
		self.dMessage.layout = QGridLayout()
		#self.dMessage.layout.setColumnStretch(1, 4)
		
		self.dMessage.layout.addWidget(QLabel(messageToDisplay))
		
		self.dMessage.horizontalGroupBox.setLayout(self.dMessage.layout)
		windowLayout = QVBoxLayout()
		windowLayout.addWidget(self.dMessage.horizontalGroupBox)
		self.dMessage.setLayout(windowLayout)
		
		self.dMessage.show()
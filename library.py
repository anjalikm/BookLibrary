import mysql.connector
import time
from datetime import date

cnx = mysql.connector.connect(user='anjali',password='anjali',host='127.0.0.1',database='library')
cursor = cnx.cursor()


def checkOutQuery(user,checklist):
	cursor = cnx.cursor()
	checkdate = date.today().isoformat()
	print(user + "checking out the book:" + str(checklist))
	#print(checklist)
	status="Checked Out"

	#check out only correct books
	tempquery = 'SELECT bookID from books where Status !="Checked Out" OR Status IS NULL'
	correctList = []
	cursor.execute(tempquery)
	for id in cursor:
		id = str(id)
		tempid = id[id.index("'")+1:id.rindex("'")]
		if(tempid in checklist):
			correctList.append(tempid)

	query = ("""UPDATE books SET User= %s, Status= %s, checkoutDate= %s WHERE bookID IN (\"""" + '","'.join(correctList) +  "\")" )
	values = (user,status,checkdate)
	print(query,values)
	cursor.execute(query,values)
	cnx.commit()
	
	
	return (True,correctList)

def getAllUsers():
	cursor = cnx.cursor()
	query ='SELECT DISTINCT User FROM books WHERE User!= ""'
	cursor.execute(query)
	userList = []
	for user in cursor:
		if(user != None ):
			userList.append(user)
	return userList


def getUserInfo(user):
	cursor = cnx.cursor()
	query = ("""SELECT bookID, Title, checkoutDate FROM books WHERE User = "%s" """) % (user)
	#print(query)
	userInfo = []
	cursor.execute(query)
	for (id,title,cDate) in cursor:
		userInfo.append((id,title,cDate))
	return userInfo


def returnQuery(user,idList):
	cursor = cnx.cursor()
	query= ("""UPDATE books SET User ="", Status="", checkoutDate=  NULL WHERE bookID IN(\"""" + '","'.join(idList) + "\")" )
	#print(query)
	cursor.execute(query)
	cnx.commit()
	return True

def existsBookId(id):
	cursor = cnx.cursor()
	query = ('SELECT Title FROM books WHERE bookID = "%s"') %(id)
	#print(query)
	cursor.execute(query)
	count = 0 
	for title in cursor:
		count = count + 1
		print(title) 
	
	return count

def addNewBook(id,title,author):
	
	query = ("""INSERT INTO books (bookID,Title,Author) VALUES("%s","%s","%s")""") % (id,title,author)
	print(query)
	cursor.execute(query)

	cnx.commit()

def findBooks(findTitle):
	query=('SELECT bookID,Title,Author,checkoutDate,Status FROM books WHERE Title LIKE "%' + findTitle + '%"')
	cursor.execute(query)
	bookDataList=[]
	for (id,title,author,cDate,st) in cursor:
		bookDataList.append((id,title,author,cDate,st))

	return(bookDataList)


	#getUserInfo("anjalik")
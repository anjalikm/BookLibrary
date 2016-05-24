import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys
import library

'''
TODOs:
1.reset fields after adding new book to database
2. find a book
3. new Book Id cannot be empty
'''

global userName,id1,id2,id3,id4,id5,varUserSelected,varUserInfo,infoListBox,user,newBookId,userList,option
global newBookId,newBookTitle,newAuthor,FrameChild

def exists():
	print('checking if the new bookid exists....' + newBookId.get())
	result  = library.existsBookId(newBookId.get())
	if result > 0 :
		messagebox.showinfo(message='Duplicate Book ID. Enter new ID')
		bNew.focus_set()

def updateUsers():
	varUserSelected.set('')
	option['menu'].delete(0,END)
	newUserList = library.getAllUsers()
	for user in newUserList:
		option['menu'].add_command(label=user, command=tkinter._setit(varUserSelected, user))

def showUserInfo(*args):
	global user
	if(varUserSelected.get() == ''):
		return
	temp  = str(varUserSelected.get())
	user = temp[temp.index("'")+1:temp.rindex("'")]
	print('current user:'+user)
	varUserInfo=library.getUserInfo(user)
	
	infoListBox.delete(0,END)
	for rec in varUserInfo:
		infoListBox.insert(END,rec)
	#print(varUserInfo)


def resetCheckoutFields():
	userName.set('')
	id1.set('')
	id2.set('')
	id3.set('')
	id4.set('')
	id5.set('')

	
def resetReturnData():
	#userList.set(null)
	#varUserSelected.set(null)
	infoListBox.delete(0,END)
	varUserInfo=library.getUserInfo(user)
	for rec in varUserInfo:
		infoListBox.insert(END,rec)

def formatCheckoutData():
	global userList
	if userName.get() == '':
		messagebox.showinfo(message='User cannot be empty')
		return
	checklist=[]
	for id in (id1,id2,id3,id4,id5):
		if id.get() != '':
			checklist.append(id.get())
	
	print(checklist)
	print(userName.get())
	
	result = library.checkOutQuery(userName.get(),checklist)
	if result[0]:
		messagebox.showinfo(message='You have successfully checked out the books:' + str(result[1:]))
	else:
		messagebox.showinfo(message='error')
	
	resetCheckoutFields()

def formatReturnData():
	global user
	print(user)	
	idList=[]
	indexes = infoListBox.curselection()
	for index in indexes:
		tempid = infoListBox.get(index)[0]
		idList.append(tempid)

	result = library.returnQuery(user,idList)
	if result:
		messagebox.showinfo(message='You have successfully returned the books')
		
	else:
		messagebox.showinfo(message='error')

	resetReturnData()


def formatAddNewBookData(id,title,author):
	if(id ==''):
		messagebox.showinfo(message="Book ID is required.")
		return
	library.addNewBook(id,title,author)
	resetAddNewBookData()

def resetAddNewBookData():
	newBookId.set('')
	newBookTitle.set('')
	newAuthor.set('')




bwidth = 20
root = Tk()
root.title("Welcome to Library")


#root row column cofiguration    
root.rowconfigure(0,weight=1)
for c in range(3):
    root.columnconfigure(c, weight=1)

Frame1 = Frame(root, bg="yellow")
Frame2 = Frame(root, bg="orange")
Frame3 = Frame(root, bg="orange")
Frame4 = Frame(root, bg="orange")

Frame1.grid(row=0,column = 0, columnspan=1,sticky = W+E+N+S)
'''
Frame2.grid(row=0,column = 1, columnspan=2,sticky = W+E+N+S)
Frame3.grid(row=0,column = 1, columnspan=2,sticky = W+E+N+S)
Frame4.grid(row=0,column = 1, columnspan=2,sticky = W+E+N+S)
'''



#right and left frames row column configuration
for r in range(20):
    Frame1.rowconfigure(r, weight=1)  
    Frame2.rowconfigure(r,weight=1) 
    Frame3.rowconfigure(r,weight=1)
    Frame4.rowconfigure(r,weight=1)


Frame1.columnconfigure(1,weight = 1)

for c in range(3):
	Frame2.columnconfigure(c,weight=1)
	Frame3.columnconfigure(c,weight=1)
	Frame4.columnconfigure(c,weight=1)

def display(win):

	print(win)
	if win == "check":
		Frame3.grid_forget()
		Frame4.grid_forget()
		Frame2.grid(row=0,column = 1, columnspan=2,sticky = W+E+N+S)

	elif win == "return":
		Frame2.grid_forget()
		Frame4.grid_forget()
		updateUsers()
		infoListBox.delete(0,END)
		Frame3.grid(row=0,column = 1, columnspan=2,sticky = W+E+N+S)
		

	elif win == "add":
		Frame2.grid_forget()
		Frame3.grid_forget()	
		Frame4.grid(row=0,column = 1, columnspan=2,sticky = W+E+N+S)




#check out frame2 design
Label(Frame2, width =30,text="Enter User Name:").grid(row =3,column=0)
userName = StringVar()
textUser = Entry(Frame2, textvariable=userName)
textUser.grid(row = 3, column=1,sticky=W)
Label(Frame2,width =30,text="Enter All book Ids:").grid(row= 5, column=0)
id1 = StringVar()
textId1 = Entry(Frame2,textvariable=id1)
textId1.grid(row=5,column=1,sticky=W)
id2 = StringVar()
textId2 = Entry(Frame2,textvariable=id2)
textId2.grid(row=7,column=1,sticky=W)
id3 = StringVar()
textId3 = Entry(Frame2,textvariable=id3)
textId3.grid(row=9,column=1,sticky=W)
id4 = StringVar()
textId4 = Entry(Frame2,textvariable=id4)
textId4.grid(row=11,column=1,sticky=W)
id5 = StringVar()
textId5 = Entry(Frame2,textvariable=id5)
textId5.grid(row=13,column=1,sticky=W)

#b = ttk.Button(Frame2, text="check out", command=lambda:library.checkOutBooks("aaa"))
b = ttk.Button(Frame2, text="Check out", command=lambda:formatCheckoutData())
b.grid(row= 16, column =2,sticky=W)



#return book frame3 design

Label(Frame3, width = 30,text="Select username:").grid(row=3,column=0)
#update the users in the option menu
varUserSelected = StringVar()
varUserSelected.trace("w",showUserInfo)
userList = library.getAllUsers()
option = OptionMenu(Frame3,varUserSelected,*userList)
varUserInfo = StringVar()
option.grid(row=3,column=1,sticky=W)
selectBooksLabel = Label(Frame3,width = 30,text="Select the books to return").grid(row=5,column=0,sticky=  N)
#frame to hold listbox and Scrollbar
FrameChild = Frame(Frame3, bg="white")
FrameChild.grid(row=5,column=1,sticky=W + N)
vertScrollbar = Scrollbar(FrameChild, orient=VERTICAL)
vertScrollbar.pack(side=RIGHT,fill =Y)

infoListBox = Listbox(FrameChild, selectmode=MULTIPLE,height = 10,width=50)
infoListBox.pack()

infoListBox.config(yscrollcommand=vertScrollbar.set)
vertScrollbar.config(command=infoListBox.yview)

submitButton = ttk.Button(Frame3,text="Submit",command=lambda:formatReturnData())
submitButton.grid(row=10,column =1,sticky=E)




# add new book Frame4 design
Label(Frame4, width =30,text="Book ID:"). grid(row=2, column=0,sticky= E)
#vlcdExist = Frame4.register(exists)
newBookId = StringVar()
textNewId = Entry(Frame4,width =30,textvariable = newBookId,validate="focusout",validatecommand=(exists))
textNewId.grid(row=2,column=1)
textNewId.focus_set()
Label(Frame4,width =30,text="Book title").grid(row=4, column=0,sticky= E)
newBookTitle = StringVar()
textNewBookTitle = Entry(Frame4,width =30,textvariable=newBookTitle)
textNewBookTitle.grid(row=4,column=1)
Label(Frame4,width =30,text="Author").grid(row=6,column=0,sticky= E)
newAuthor = StringVar()
textNewAuthor = Entry(Frame4,width =30,textvariable=newAuthor)
textNewAuthor.grid(row=6,column=1)
bNew = ttk.Button(Frame4, text="Add", command=lambda:formatAddNewBookData(newBookId.get(),newBookTitle.get(),newAuthor.get()))
bNew.grid(row=10,column=2)






# right frame buttons 
btnCheckout = ttk.Button(Frame1, text="Check out",command=lambda:display("check"))
btnCheckout.grid(column=1, row=8)
btnCheckout.configure(width=bwidth)

btnRerurn = ttk.Button(Frame1, text="Return the Books", command=lambda:display("return"))
btnRerurn.grid(column=1, row=10)
btnRerurn.configure(width=bwidth)

btnAddNew = ttk.Button(Frame1, text="Add New Book", command=lambda:display("add"))
btnAddNew.grid(column=1, row=12)
btnAddNew.configure(width=bwidth)

btnFindBook = ttk.Button(Frame1, text="Find a book", command=lambda:display("find"))
btnFindBook.grid(column=1, row=14)
btnFindBook.configure(width=bwidth)













root.mainloop()
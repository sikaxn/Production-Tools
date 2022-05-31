# coding: utf-8
import urllib.request,json
import urllib.parse
from random import randint
import time
import os
from urllib.request import unquote
from html import unescape



def randNumN(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def nwkConnectionInit():
    
    ipaddr = "127.0.0.1"
    port = "8089"
    SessionID = randNumN(6)
    print("Init network")
    url = "http://" + ipaddr + ":" + str(port) + "/update.aspx?sessionID=" + str(SessionID) + "&filter=&page=1&queue=true" 
    print(url)
    global req
	
    req = urllib.request.Request(url)
    try:
        print("Connecting...\n")
        read = urllib.request.urlopen(req).read()
        print("Connected...\n")
    except:
        print("Network Connection issue! \n")
        return 1
    return 0
    
def updateRawGet():
    try:
        read = urllib.request.urlopen(req).read()
        
       ## #print(read)
        return read
    except:
        return 0

def stripEmptyData(input):
	input = str(input)
	strlengh = len(input)
	###print (strlengh)
	if strlengh <= 100:
		return 0
	elif strlengh >= 100 and  strlengh <= 180:
		return 1
	else:
		return input

def stripQueuedData(input):
	keyword ="nbsp"
	QueueCount = input.count(keyword)
	###print("current cue:")
	###print(QueueCount)
	###print("_________start of cycle_____________________________")


	###print("_________input_____________________________")
	index = 0
	loc =[]
	
	for i in range(QueueCount):
		index = input.find(keyword,index)
		if index == -1:
			break
		###print ("key found", index)
		loc.append(index)
		index += len(keyword)
		###print(loc)
		###print("______________________________________")
	for i in range(QueueCount):
		#print(i)
		if QueueCount == 1:
			###print(loc[0])
			strout = input[loc[0]:]
		else:
			if i==0:
				###print("aaaaaaa")
				###print(loc[0],loc[1])
				strout = input[loc[0]:loc[1]]
			
			elif i==QueueCount -1 :
				###print("bbbbbb")
				
				strout = input[loc[i]:]
				
			else:
				###print("cccccc")
				nextLoc = int(loc[i + 1]) 
				strout = input[loc[i]:loc[i+1]]
			
		###print("!!!!!!!!!")
		###print(strout)
		Msg = msgDecode(strout)
		strMsg = str(Msg)
		hashMsg = hash(strMsg)
		if hashMsg not in allDataHashStr:
			allDataStr.append(Msg)
			allDataHashStr.append(hashMsg)
			###print("new found, #printing!")
			###print(strMsg)
			printingHandler(Msg)
		###print(allDataStr)
		###print(allDataHashStr)
		###print("!!!!!!!!!")
		
	###print("_________end of cycle_____________________________")
	
def pageMgmt(input):
	newstr = input
	strLengh = len(newstr)
	PNLocation = strLengh - 7
	beginningSign = "setPaging("
	enddingSign = ","
	
	PageNumber = newstr[PNLocation]
	###print("current Page Number:")
	###print(PageNumber)
	###print("+-+-+-+-+-+-+-+-+-")
	
	
def msgDecode(msgIn):
	msgOut =["Name","Time","Content"]
	msgLen = len(msgIn)
	##print(msgIn)
	##find Name

	nameLoc = 14
	###print("+-+-+-+-nameLoc+-+-+-+-+-")
	###print (nameLoc)
	nameEndKey = "</td>"
	nameEndLoc = int(msgIn.find(nameEndKey,nameLoc))
	##print("+-+-+-+-nameEndLoc+-+-+-+-+-")
	##print (nameEndLoc)
	name = msgIn[nameLoc:nameEndLoc]
	name = unescape(unquote(name))
	##print("name")
	##print(name)
	##Find Time
	timeKey = "data-date"
	timeLoc = msgIn.find(timeKey , nameLoc)
	timeEndKey = "\'>"
	timeEndLoc = int(msgIn.find(timeEndKey, timeLoc))
	time = msgIn[timeLoc + 12 :timeEndLoc - 1 ]
	###print (timeLoc)
	###print (timeEndLoc)
	##print("time")
	##print (time)
	##Find Content
	contKey = "</td><td>"
	contEndKey = "</td><td data-dat"
	conLoc = msgIn.find(contKey , nameEndLoc)
	##print (conLoc)
	contEndLoc = int(msgIn.find(contEndKey,conLoc))
	content = msgIn[conLoc +9 :contEndLoc]
	content = unescape(unquote(content))
	##print("content")
	##print(content)
	##print("+-+-+-+-+-+-+-+-+-")
	msgOut = [name,time,content]
	###print (msgOut)
	return msgOut
	
	
def printingHandler(listIn):
	###print(listIn)
	name = listIn[0]
	time = listIn[1]
	content = listIn[2]
	print(name)
	print(time)
	print(content)
	with open('nopol.txt', 'w') as f:
            towrite = "----NEW CUE----\n \n" +"Time: " + time+ "\n\nName: " +name + " \n ------------ \n" + content + "\n------------ \n" +  "----END----"
            f.write(towrite)
	os.system('python Pprint.py')
	
def printingCleared():
	with open('nopol.txt', 'w') as f:
            towrite = "----\nCleared\n---- "
            f.write(towrite)
	os.system('python Pprint.py')

def printingReady():
	with open('nopol.txt', 'w') as f:
            towrite = "----\nReady\n---- "
            f.write(towrite)
	os.system('python Pprint.py')


nwkConnectionInit()
global allDataStr
global allDataHashStr
allDataStr = []
allDataHashStr = []
clrPrinted =1
##printingReady()
while True:
	newstr = stripEmptyData(updateRawGet())
	if newstr == 1:
		allDataStr = []
		allDataHashStr = []
		os.system('cls||clear')
		print("cleared")
		if clrPrinted ==1:
			printingCleared()
			clrPrinted = 0
	elif newstr !=0:
		clrPrinted = 1
		os.system('cls||clear')
		##pageMgmt(newstr)
		##print("newstr")
		stripQueuedData(newstr)
	time.sleep(0.3)
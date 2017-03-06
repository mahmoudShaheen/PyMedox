#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				 python-MYSQL interface						#
 ###########################################################

import sqlite3
import data #to use data using data.x 'change occurs here is limited to here'
from time import strftime
import datetime
import time

#Get current time "returns hours, minutes"
def getCTime():
	h = strftime("%H")
	m = strftime("%M")
	s = strftime("%S")
	currentTime = [h,m,s]
	return currentTime

#Get the next time bills will be dispensed
def getNextSchedule():
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	hmTime=getCTime()
	h=int(hmTime[0])
	m=int(hmTime[1])
	s=int(hmTime[2])
	rTime=datetime.timedelta(hours=h,minutes=m,seconds=s)
	sql = """SELECT `time` FROM `timetable`
		ORDER BY `time` ASC"""
	curs.execute(sql)
	close(db)
	tempTimeArray = curs.fetchall()
	if (len(tempTimeArray) == 0): #return false if timetable is empty
		return False
	timeArray = []
	for row in tempTimeArray:
		timeArray.append(row[0])
	print "time array:\n" , timeArray
	if(len(timeArray) > 0 ):
		if (rTime > timeArray[-1]): #if currentTime > last item in ordered array "dispensing finished for today"
			print"min: ",  timeArray[0]
			resetDispensed() #mark all drugs as not dispensed "as this is the end of the day"
			return timeArray[0]
		else:
			for row in timeArray:
				if (row > rTime):
					print"row: " , row
					return row
	return false;

#returns array of number of bills for every warehouse medicine which should be dispensed
def getBills(rTime):
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()

	sql = """SELECT `bill_array` FROM `timetable` 
		WHERE `time` = '%s' """ % (rTime)
	curs.execute(sql)
	billString = curs.fetchone()
	billArray = billString.split(",") #convert string to array by separator ","
	bills = [int(i) for i in r] #convert the string array to int array
	close(db)
	return bills

def checkBills(bills): #check if the bills in the box will be enough for the schedule, accepts array of bills [1,0,2,0]
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	
	for i in range(1,data.warehouseCount+1): #1 for id to start from 1
		sql = """SELECT `bill_count` FROM `warehouse` 
				WHERE `id` = '%d' """ % (i)
		curs.execute(sql)
		remainingBills = curs.fetchone()
		if bills[i-1] > remainingBills:
			close(db)
			return False
	close(db)
	return True

def subtractBills(bills): #update bill_count after dispensing, accepts array of bills [1,0,2,0]
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	for i in range(1,data.warehouseCount+1): #1 for id to start from 1
		sql = """SELECT `bill_count` FROM `warehouse` 
				WHERE `id` = '%d' """ % (i)
		curs.execute(sql)
		remainingBills = curs.fetchone()
		newValue = remainingBills - bills[i-1]
		
		sql = """UPDATE warehouse SET  
			bill_count='%d' 
			WHERE id = '%d'"""%(newValue,i)
		curs.execute(sql)
	close(db)

def markDispensed(rtime): #mark a time as dispensed
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()	
	sql = """UPDATE timetable SET  
			`dispensed` ='%d' 
			WHERE `time` = '%s'"""%(1,rTime)
	curs.execute(sql)
	close(db)

def resetDispensed():
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	sql = """UPDATE `timetable` SET	
			`dispensed` = '%d'"""%(0)
	curs.execute(sql)
	close(db)

def isDispensed(rTime):
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	sql = """SELECT `dispensed` FROM `timetable`
			WHERE `time` = '%s'"""%(rTime)
	curs.execute(sql)
	tempDis = curs.fetchone()
	close(db)
	return tempDis[0]

def close(db):
	db.commit()
	db.close()

def clearTimetable():
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	data.scheduleChanged = True
	curs.execute("DELETE FROM timetable")
	tempDis = curs.fetchone()
	close(db)
	
def refreshTimetable(timeArray, drugArray):
	clearTimetable()
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	i = 0
	for row in timeArray:
		sql = """"INSERT INTO `timetable` (id ,time, bill_array, dispensed)
			VALUES ('%d', '%s', '%s', '%d'),;""" % (i+1, timeArray[i], drugArray[i], 0) #i+1 for id to start from 1
		curs.execute(sql)
	close(db)

def addBills(billArray):
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	for i in range(1,data.warehouseCount+1): #1 for id to start from 1
		sql = """SELECT `bill_count` FROM `warehouse` 
				WHERE `id` = '%d' """ % (i)
		curs.execute(sql)
		remainingBills = curs.fetchone()
		newValue = remainingBills + bills[i-1]
		sql = """UPDATE warehouse SET  
			bill_count='%d' 
			WHERE id = '%d'"""%(newValue,i)
		curs.execute(sql)
	close(db)

def clearBills():
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	for i in range(1,data.warehouseCount+1): #1 for id to start from 1
		sql = """UPDATE warehouse SET  
			bill_count='%d' 
			WHERE id = '%d'"""%(0,i)
		curs.execute(sql)
	close(db)

def getBillCount():
	db = sqlite3.connect(data.dbName)
	curs = db.cursor()
	billCount = ""
	for i in range(1,data.warehouseCount+1): #1 for id to start from 1
		sql = """SELECT `bill_count` FROM `warehouse` 
				WHERE `id` = '%d' """ % (i)
		curs.execute(sql)
		remainingBills = curs.fetchone()
		billCount = billCount + str(remainingBills) + ","
	billCount = billCount[:-1] #remove the last ","
	return billCount

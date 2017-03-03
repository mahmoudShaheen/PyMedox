#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				 python-MYSQL interface						#
 ###########################################################

#replace/add to #db.rollback error handling function 
#add dbLock to wait for connection and disconnection

#to import MySQLdb from path
import os, sys
lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
sys.path.append("MySQLdb")

import MySQLdb

import data #to use data using data.x 'change occurs here is limited to here'
from data import db, curs #to use it without data.db or data.curs 'change occur in here changes the original data'
from time import strftime
import datetime
import time

#connect to database and save parameters to data module
def connect():
	try:
		data.db = MySQLdb.connect(data.host, data.user, data.password, data.dbName)
		data.curs=db.cursor()
		time.sleep(data.dbDelay)
	except:
		print 'error connecting to db-retrying'
		connect()
	
#close database connection
def disconnect():
	data.db.close()
	time.sleep(data.dbDelay)

#Get current time "returns hours, minutes"
def getCTime():
	h = strftime("%H")
	m = strftime("%M")
	s = strftime("%S")
	currentTime = [h,m,s]
	return currentTime

#Get the next time bills will be dispensed
def getNextSchedule():
	try:
		hmTime=getCTime()
		h=int(hmTime[0])
		m=int(hmTime[1])
		s=int(hmTime[2])
		rTime=datetime.timedelta(hours=h,minutes=m,seconds=s)
		sql = """SELECT `time` FROM `timetable`
			ORDER BY `time` ASC"""
		curs.execute(sql)
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
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback() 
	time.sleep(data.dbDelay)


#returns array of number of bills for every warehouse medicine which should be dispensed
def getBills(rTime):
	try:
		sql = """SELECT `id` FROM `timetable` 
			WHERE `time` = '%s' """ % (rTime)
		curs.execute(sql)
		timeID = curs.fetchone()
		timeID = timeID[0]
		time.sleep(data.dbDelay)
		sql = """SELECT `warehouse_id`  FROM `connection` WHERE 
			`time_id` = '%d' """ % (timeID)
		curs.execute(sql)
		tempBills = curs.fetchall()

		for i in range(0,data.warehouseCount):
			bills[i]=0
		for row in tempBills:
			bills[row[0]-1] += 1
		#for row in tempBills:
		#	bills.append(row[0])
		print bills
		db.commit()
		return bills
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

def checkBills(bills): #check if the bills in the box will be enough for the schedule
	try:
		for row in bills:
			sql = """SELECT `bill_count` FROM `warehouse` 
					WHERE `id` = '%d' """ % (row+1)
			curs.execute(sql)
			time.sleep(data.dbDelay)
			remainingBills = curs.fetchone()
			if bills[row] > remainingBills:
				return False
		return True
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

def subtractBills(bills): #update bill_count after dispensing
	try:
		for row in bills:
			sql = """SELECT `bill_count` FROM `warehouse` 
					WHERE `id` = '%d' """ % (row+1)
			curs.execute(sql)
			remainingBills = curs.fetchone()
			newValue = remainingBills - bills[row]
			time.sleep(data.dbDelay)
			sql = """UPDATE warehouse SET  
				bill_count='%d' 
				WHERE id = '%d'"""%(newValue,row+1)
			curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

def markDispensed(rtime): #mark a time as dispensed
	try:
		sql = """UPDATE timetable SET  
				`dispensed` ='%d' 
				WHERE `time` = '%s'"""%(1,rTime)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

def resetDispensed():
	try:
		sql = """UPDATE `timetable` SET	
				`dispensed` = '%d'"""%(0)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

def isDispensed(rTime):
	try:
		sql = """SELECT `dispensed` FROM `timetable`
				WHERE `time` = '%s'"""%(rTime)
		curs.execute(sql)
		time.sleep(data.dbDelay)
		tempDis = curs.fetchone()
		return tempDis[0]
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

#check if a change is made in warehouse in db to reset schedule
def statusWarehouseCheck():
	try:
		sql = """SELECT `warehouse` FROM `updated` 
			WHERE `id` = %d"""%(0)
		curs.execute(sql)
		status = curs.fetchone()
		#status = status[0]
		return status
	except:
		print "\nERROR: statusWarehouseCheck OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

#check if a command is available in db to execute it
def statusCommandCheck():
	try:
		sql = """SELECT `command` FROM `updated` 
			WHERE `id` = %d"""%(0)
		curs.execute(sql)
		status = curs.fetchone()
		#status = status[0]
		return status
	except:
		print "\nERROR: statusCommandCheck OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

#get commands for box and delete it
def getCommands():
	try:
		sql = "SELECT `command` FROM `command`"
		curs.execute(sql)
		command = curs.fetchall()
		return command
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.dbDelay)

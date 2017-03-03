#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				 python-MYSQL interface						#
 ###########################################################

#to import MySQLdb from path
import os, sys
lib_path = os.path.abspath(os.path.join('..', '..', '..', 'lib'))
sys.path.append("MySQLdb")

import MySQLdb

import data #to use data using data.x 'change occurs here is limited to here'
from data import db, curs #to use it without data.db or data.curs 'change occur in here changes the original data'
from time import strftime, strptime
import datetime
import time
from data import db, curs



#connect to database and save parameters to data module
def connect():
	try:
		data.db = MySQLdb.connect(data.host, data.user, data.password, data.dbName)
		data.curs=db.cursor()
		time.sleep(data.delay)
	except:
		print 'error connecting to db-retrying'
		connect()
	
#close database connection
def disconnect():
	data.db.close()
	time.sleep(data.delay)

#initialize tables with default values "in fact it just initialize with warehouse table"
def initializeTables():
	try:
		curs.execute("DELETE FROM warehouse")
		curs.execute("ALTER TABLE warehouse AUTO_INCREMENT=1")
		db.commit()
		for i in range(1,data.warehouseCount+1):
			drugName = "drug(%d)"%(i)
			sql =  """INSERT INTO warehouse 
				(drug_name, bill_count) 
				Values('%s',NULL);""" % (drugName)
			curs.execute (sql)
			db.commit() 
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#delete all entries from all tables and re-initialize tables
def resetSchedule():
	try:
		curs.execute("DELETE FROM warehouse")
		curs.execute("DELETE FROM timetable")
		curs.execute("DELETE FROM connection")
		curs.execute("ALTER TABLE warehouse AUTO_INCREMENT=1")
		curs.execute("ALTER TABLE timetable AUTO_INCREMENT=1")
		db.commit()
		initializeTables()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#change drug name in warehouse table "also add new one instead of default values"
def editDrugName(id,name,bill_count):
	try:
		sql = """UPDATE warehouse SET 
			drug_name = '%s', 
			bill_count='%d' 
			WHERE id = '%d'"""%(name,bill_count,id)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#add time in the timetable table
def addTime(time):
	try:
		sql = """INSERT INTO timetable 
			SET time = '%s'""" %(time)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#replace a time with a a new one "without affecting bills connected to it" 
def changeTime(oldTime,newTime):
	try:
		sql = """UPDATE `timetable` 
			SET `time` = '%s' 
			WHERE `time` = '%s'""" % (newTime,oldTime)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#delete a time from timetable table "also any connection in the connection table with it will be deleted"
def deleteTime(time):
	try:
		sql = """SELECT `id` 
			FROM `timetable` 
			WHERE `time` = '%s' """ % (time)
		curs.execute(sql)
		id = curs.fetchone()
		id = id[0]
		time.sleep(data.delay)
		sql = """DELETE FROM `connection` 
			WHERE `time_id` = '%d'""" % (id)
		curs.execute(sql)
		time.sleep(data.delay)
		sql = """DELETE FROM `timetable` 
			WHERE `id` = '%d'""" % (id)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#add new entry to connection table
def addEntry(time,drugName,billCount):
	try:
		sql = """SELECT `id` 
			FROM `timetable` 
			WHERE `time` = '%s'""" % (time)
		curs.execute(sql)
		timeID = curs.fetchone()
		timeID = timeID[0]
		time.sleep(data.delay)
		sql = """SELECT `id` 
			FROM `warehouse` 
			WHERE `drug_name` = '%s'""" % (drugName)
		curs.execute(sql)
		warehouseID = curs.fetchone()
		warehouseID = warehouseID[0]
		print timeID
		print warehouseID
		for i in range(1,billCount+1):
			print i
			time.sleep(data.delay)
			sql = """INSERT INTO `connection` SET 
				`time_id` = '%d', 
				`warehouse_id` = '%d' """ % (timeID, warehouseID)
			curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#delete orphan time entries from timetable table
def wipeEmpty():
	try:
		sql = """SELECT `id` 
			FROM `timetable`"""
		curs.execute(sql)
		id = curs.fetchall()
		for row in id:
			tempID=row[0]
			time.sleep(data.delay)
			sql = """DELETE FROM `timetable` 
				WHERE  `id` = '%d'
					  AND NOT EXISTS(
						SELECT `time_id` FROM `connection` 
							where `time_id` = '%d');""" % (tempID,tempID)
			curs.execute(sql)
			db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#delete entry from connection table "also delete orphan time entries from timetable table "
def deleteEntry(time,drugName):
	try:
		sql = """SELECT `id` FROM `timetable` 
			WHERE `time` = '%s'""" % (time)
		curs.execute(sql)
		timeID = curs.fetchone()
		timeID = timeID[0]
		time.sleep(data.delay)
		sql = """SELECT `id` FROM `warehouse` 
			WHERE `drug_name` = '%s'""" % (drugName)
		curs.execute(sql)
		warehouseID = curs.fetchone()
		warehouseID = warehouseID[0]
		time.sleep(data.delay)
		sql = """DELETE FROM `connection` WHERE 
			`time_id` = '%d' 
			AND `warehouse_id` = '%d' """ % (timeID, warehouseID)
		curs.execute(sql)
		db.commit()
		wipeEmpty()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

#delete drug from all times "connection table", leave it in warehouse, delete orphan time entries
def deleteDrug(drugName):
	try:
		sql = """SELECT `id` FROM `warehouse` 
			WHERE `drug_name` = '%s'""" % (drugName)
		curs.execute(sql)
		id=curs.fetchone()
		id=id[0]
		time.sleep(data.delay)
		sql = """DELETE FROM `connection` 
			WHERE `warehouse_id` = '%d'""" % (id)
		curs.execute(sql)
		db.commit()
		wipeEmpty()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

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
	time.sleep(data.delay)


#returns array of number of bills for every warehouse medicine which should be dispensed
def getBills(rTime):
	try:
		sql = """SELECT `id` FROM `timetable` 
			WHERE `time` = '%s' """ % (rTime)
		curs.execute(sql)
		timeID = curs.fetchone()
		timeID = timeID[0]
		time.sleep(data.delay)
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
	time.sleep(data.delay)

#returns the full schedule
def getFullSchedule():
	try:
		sql = """ SELECT t.time AS Time, w.drug_name AS Medications
			FROM `timetable` AS t 
			LEFT JOIN connection AS c
			ON t.id = c.time_id 
			LEFT JOIN `warehouse` AS w 
			ON c.warehouse_id =w.id;""" 
		curs.execute(sql)
		schedule = []
		print "\nTime	      Medication"
		print "========================="
		for reading in curs.fetchall():
			print str(reading[0]),"\t",str(reading[1])
			schedule.append(str(reading[0]))
			schedule.append(str(reading[1]))
		print schedule
		return schedule
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

def checkBills(bills): #check if the bills in the box will be enough for the schedule
	for row in bills:
		sql = """SELECT `bill_count` FROM `warehouse` 
				WHERE `id` = '%d' """ % (row+1)
		curs.execute(sql)
		time.sleep(data.delay)
		remainingBills = curs.fetchone()
		if bills[row] > remainingBills:
			return False
	return True

def subtractBills(bills): #update bill_count after dispensing
	try:
		for row in bills:
			sql = """SELECT `bill_count` FROM `warehouse` 
					WHERE `id` = '%d' """ % (row+1)
			curs.execute(sql)
			remainingBills = curs.fetchone()
			newValue = remainingBills - bills[row]
			time.sleep(data.delay)
			sql = """UPDATE warehouse SET  
				bill_count='%d' 
				WHERE id = '%d'"""%(newValue,row+1)
			curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

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
	time.sleep(data.delay)

def resetDispensed():
	try:
		sql = """UPDATE `timetable` SET	
				`dispensed` = '%d'"""%(0)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

def isDispensed(rTime):
	sql = """SELECT `dispensed` FROM `timetable`
			WHERE `time` = '%s'"""%(rTime)
	curs.execute(sql)
	time.sleep(data.delay)
	tempDis = curs.fetchone()
	return tempDis[0]

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
	time.sleep(data.delay)

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
	time.sleep(data.delay)

#get commands for box and delete it
def getCommands():
	try:
		sql = """SELECT `command` FROM `command` 
			WHERE `receiver` = %d"""%(0)
		curs.execute(sql)
		command = curs.fetchall()
		time.sleep(data.delay)
		sql = """DELETE FROM `command` 
			WHERE `receiver` = %d"""%(0)
		curs.execute(sql)
		return command
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

def resetwarehouseStatus():
	try:
		sql = """UPDATE `updated` SET 
			warehouse = '%d', 
			WHERE `id` = '%d'"""%(0,0)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

def resetcommandStatus():
	try:
		sql = """UPDATE `updated` SET 
			command = '%d', 
			WHERE `id` = '%d'"""%(0,0)
		curs.execute(sql)
		db.commit()
	except:
		print "\nERROR: OPERATION FAILED ! \n"
		#db.rollback()
	time.sleep(data.delay)

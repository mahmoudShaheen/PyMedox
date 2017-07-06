#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  		  Sync								#
#################################

#to receive changes in timetable and sync FDB with SQLite

import data
from pythonSQL import *
from billCount import *
import firebase

import json

#updates SQLite db by parsing timetable from FDB, Delete SQLite old timetable data and adds the new data to it
def syncdb():
	newTimetable = firebase.get(data.timetableURL) #get timetable from FDB
	if newTimetable is not None: #if the class is empty the parsed data is None
		timeArray = [] #for time values
		drugArray = [] #for drug Array
		print newTimetable
		for key, value in newTimetable.iteritems():
			timeArray.append(str(value['time']))
			drugArray.append(str(value['billArray']))
			print "time: " + str(value['time']) + ", billArray: " + str(value['billArray'])
		refreshTimetable(timeArray, drugArray) #empty timetable in SQLite, and adds the new values
		checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
	if newTimetable is None: #deleted class
		timeArray = [] #for time values
		drugArray = [] #for drug Array
		print "empty timetable"
		print newTimetable
		refreshTimetable(timeArray, drugArray) #empty timetable in SQLite, and adds the new values
		checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db

def syncNow(args):
	data.waitForSync = True
	syncdb()
	data.scheduleChanged = True
	data.waitForSync = False

def syncStart():
	S = firebase.subscriber(data.timetableURL, syncNow)  #when timetable class changes in FDB it calls syncNow
	S.start()  #start the subscriber

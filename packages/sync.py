#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  		  Sync								#
 ###########################################################

#to receive changes in timetable and sync FDB with SQLite

import data
from pythonSQL import *
from billCount import *
import firebase

#updates SQLite db by parsing timetable from FDB, Delete SQLite old timetable data and adds the new data to it
def syncdb():
	rcvData = firebase.get(data.timetableURL) #get timetable from FDB
	if rcvData is not None: #if the class is empty the parsed data is None
		io = StringIO
		timetable = json.dumps(rcvData, io) #convert data to string instead of list
		timetable = timetable[1:-1] #removes [] from data
		timetable = timetable.split(', {') #split string to JSON objects style #JSON.loads accepts only one object at a time
		timeArray = [] #for time values
		drugArray = [] #for drug Array
		for row in timetable:
			temp = json.loads('{' + row) #create JSON object
			time = temp.get('time') #get value by key
			uncodedTime = unicodedata.normalize('NFKD', time).encode('ascii','ignore')
			timeArray.append(uncodedTime) #the returned value is Unicode 
			drug = temp.get('drug') #get value by key
			uncodedDrug = unicodedata.normalize('NFKD', drug).encode('ascii','ignore')
			drugArray.append(uncodedDrug) #the returned value is Unicode 
		refreshTimetable(timeArray, drugArray) #empty timetable in SQLite, and adds the new values
		checkDay() #checks if bills in warehouse are enough for one day

def syncNow():
	data.waitForSync = True
	syncdb()
	data.scheduleChanged = True
	data.waitForSync = False

def syncStart():
	S = firebase.subscriber(data.timetableURL, syncNow)  #when timetable class changes in FDB it calls syncNow
	S.start()  #start the subscriber

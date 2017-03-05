#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  		  Sync								#
 ###########################################################

#to receive changes in timetable and sync FDB with SQLite

import data

#updates SQLite db by parsing timetable from FDB, Delete SQLite old timetable data and adds the new data to it
def syncdb():
	return

def syncNow():
	data.waitForSync = True
	syncdb()
	scheduleChanged = True
	data.waitForSync = False

def syncStart():
	S = firebase.subscriber(data.timetableURL, syncNow)  #when timetable class changes in FDB it calls syncNow
	S.start()  #start the subscriber

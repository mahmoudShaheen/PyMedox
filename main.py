#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				 	 python Server							#
 ###########################################################

from pythonSQL import *
from sync import *
from controlHardware import *
from command import commandStart
import data

import threading
import time #for time.sleep
import datetime #for datetime.timedelta
	
def timeDiff(rTime): #Calculates time difference between received and current time in Seconds
	if (rTime != False):
		hmTime=getCTime()
		h=int(hmTime[0])
		m=int(hmTime[1])
		s=int(hmTime[2])
		nTime=datetime.timedelta(hours=h,minutes=m, seconds=s)
		oneDay = datetime.timedelta(hours=24,minutes=0, seconds=0)
		if (rTime >= nTime):
			timeDifference = rTime - nTime
		if (rTime < nTime):
			timeDifference = oneDay - nTime + rTime
		return timeDifference.total_seconds()
	return False

#####will change
#sync thread checks updated table in database to check for commands and update data.data.avaliableCommand
def callSyncThread():
	syncThread = threading.Thread(target=syncStart)
	syncThread.start()
	print 'hi from callSyncThread'

#start dispensing process in new thread
def callDispenseBills(rTime):
	print 'main.callDispenseBills called'
	dispenseThread = threading.Thread(target=dispenseBills, args=(rTime,))
	dispenseThread.start()

#schedulerThread:: after a delay it calls schedulerJob
#the delay is time to the next schedule
def callSchedulerThread(rTime):
	print 'call SchedulerThread Time: ', rTime
	data.schedulerAlive = True
	schedulerThread = threading.Timer(rTime, schedulerJob)
	schedulerThread.start()
	print 'callSchedulerThread'

#tells the program that now is the time to dispense through data.schedulerCheck
#and also tells that it finished through data.schedulerAlive
def schedulerJob():
	data.schedulerCheck = True
	data.schedulerAlive = False
	print 'scheduler job called'

def mainProgram():
	while (True):
		time.sleep(data.mainLoopDelay) #to avoid errors and save resources
		##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##################################################

		#checks if  user changed schedule or dispense completed
		#to reset scheduler and gets next time to start a new scheduler Thread
		if (data.scheduleChanged == True): #if user changed schedule or dispense completed
			# A) stop current SchedulerThread
			if (data.schedulerAlive):
				schedulerThread.cancel()
			nTime = getNextSchedule() # B) get next Time
			# C) checks if timetable has entries
			if (nTime == False): #if it has no entries: set data.emptyTimetable to stop the checking process
				data.emptyTimetable = True
			else: #if it has entries: re-set data.emptyTimetable to re-start the checking process
				data.emptyTimetable = False
			# D) reset scheduler Variables to start new schedulerThread
			data.schedulerCheck = False #re-set data.schedulerCheck as false
			data.scheduleChanged = False #re-set data.scheduleChanged status to false
		
		##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##################################################
		
		#scheduler handling
		if (not data.emptyTimetable and not data.waitForDispense): #if timetable isn't marked empty && no dispensing is running
			if(data.schedulerCheck == False): #thread not marked finished
				delayToNextDispense = timeDiff(nTime)
				if (data.schedulerAlive):	#but alive -> do other work 
					#updateTimeLCD(delayToNextDispense) #'controlHardware'
				else: 					#and not alive -> Dispense and call a new schedulerThread
					if not (data.schedulerAlive): #no scheduler is running
						if (isDispensed(nTime)=='0'): #not dispensed
							callSchedulerThread(delayToNextDispense)
			######error here not called
			else: #thread finished -> start new dispense process for next time
				print 'just b4 calling dispense'
				callDispenseBills(nTime) #'controlHardware'
				data.schedulerCheck = False
				data.scheduleChanged = True #to call scheduler for next time
		
		##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##################################################

#defines global variables used in the program,
#connect to the database, and calls syncThread
schedulerThread	= threading.Thread(target=schedulerJob)
syncThread = threading.Thread(target=syncStart)
dispenseThread = threading.Thread(target=dispenseBills, args='0:0')


#time.sleep(data.osDelay) #wait for OS to work properly and database initialization
connect() #connect to database
commandStart() #start command subscriber to execute commands as soon as it arrives in the FDB
callSyncThread() #call syncThread here as is_alive and isAlive ain't working well
mainProgram()

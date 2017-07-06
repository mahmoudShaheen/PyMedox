#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				 	 python Server						#
#################################

import os, sys, inspect

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"packages")))
sys.path.insert(0, cmd_subfolder)

from pythonSQL import *
from sync import syncStart
from control import controlStart, sendSensorDataStart
from controlHardware import *
from billCount import *
from command import *
import data

import threading
import time #for time.sleep
import datetime #for datetime.timedelta
	
def timeDiff(rTime): #Calculates time difference between received and current time in Seconds
	#convert rTime: str to time delta
	h,m,s = rTime.split(':') #split the time string by ':'
	rTime = datetime.timedelta(hours=int(h),minutes=int(m),seconds=int(s)) #convert h,m,s to ints then to timedelta object
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

#start dispensing process in new thread
def callDispenseBills(rTime):
	print 'main.callDispenseBills called'
	dispenseThread = threading.Thread(target=dispenseBills, args=(rTime,))
	dispenseThread.start()

#schedulerThread:: after a delay it calls schedulerJob
#the delay is time to the next schedule
def callSchedulerThread(rTime):
	try:
		schedulerThread.cancel()
	except:
		print "trying to cancel not started thread: SchedulerThread"
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
		if(not data.emptyTimetable) and (not data.emptyWarehouse): #if timetable isn't marked empty && warehouse has enough bills
			if (not data.waitForSync) and (not data.waitForCmd) and (not data.waitForDispense): #if sync and commands threads aren't changing anything do the following
				if(data.dispense):
					data.dispense
					data.schedulerCheck = True
					data.dispense = False
					schedulerThread.cancel()
					data.schedulerAlive = False
					print "dispenseNext command detected, scheduler Cancelled"
					print "schedulerCheck: ", data.schedulerCheck
					print "dispenseNext: ", data.dispense
					
				##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##################################################

				#checks if  user changed schedule or dispense completed
				#to reset scheduler and gets next time to start a new scheduler Thread
				if (data.scheduleChanged == True): #if user changed schedule or dispense completed
					# A) stop current SchedulerThread
					if (data.schedulerAlive):
						schedulerThread.cancel()
						#schedulerThread.join()
						data.schedulerAlive = False
						print "scheduler Cancelled"
					nTime = getNextSchedule() # B) get next Time
					# C) checks if timetable has entries
					if (nTime == False): #if it has no entries: set data.emptyTimetable to stop the checking process
						data.emptyTimetable = True

					# D) reset scheduler Variables to start new schedulerThread
					data.schedulerCheck = False #re-set data.schedulerCheck as false
					data.scheduleChanged = False #re-set data.scheduleChanged status to false
				
				##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##################################################
				
				#scheduler handling
				if(data.schedulerCheck == False): #thread not marked finished
					delayToNextDispense = timeDiff(nTime)
					if (data.schedulerAlive):	#but alive -> do other work 
						updateTimeLCD(delayToNextDispense) #'controlHardware'
					else: 					#and not alive -> Dispense and call a new schedulerThread
						if not (data.schedulerAlive): #no scheduler is running
							if (isDispensed(nTime)== 0): #not dispensed
								callSchedulerThread(delayToNextDispense)
				######error here not called
				else: #thread finished -> start new dispense process for next time
					print 'just b4 calling dispense'
					callDispenseBills(nTime) #'controlHardware'
					data.schedulerCheck = False
					data.scheduleChanged = True #to call scheduler for next time
			
				##################################################@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##################################################
			else:
				print "main waiting"
				print "waitForCmd: ", data.waitForCmd
				print "waitForSync" , data.waitForSync
				print "waitForDispense" , data.waitForDispense
		else:
			print "main waiting: Empty"
			print "emptyTimetable: ", data.emptyTimetable
			print "emptyWarehouse" , data.emptyWarehouse
				
#defines global variables used in the program,
schedulerThread = threading.Timer(60, schedulerJob)
dispenseThread = threading.Thread(target=dispenseBills, args='0:0')

#time.sleep(data.osDelay) #wait for OS to work properly
commandStart() #start command subscriber to execute commands as soon as it arrives in the FDB
syncStart() #start sync subscriber to sync FDB with SQLite as soon as FDB changes 
#time.sleep(60)
#controlStart() #start control thread to update switches states as soon as FDB changes 
#sendSensorDataStart() #send sensor data to db every data.sensorDelay seconds
#checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
mainProgram() #call main program

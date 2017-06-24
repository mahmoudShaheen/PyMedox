#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				   Control Hardware						#
#################################

from pythonSQL import *
from notification import *
from billCount import *
import data

import subprocess #for calling restart shell script

import threading #for timer thread
import datetime #for datetime.timedelta
doorDelay = datetime.timedelta(minutes=5,seconds=0) #5 minutes then send door not opened notification
timerThread = threading.Timer(doorDelay, target=doorNotOpenedNotification) #to check if door not opened for 5 minutes

def dispenseBills(rTime):
	print 'dispensing Bills Called'
	data.waitForDispense = True
	bills = getBills(rTime)
	check = checkBills(bills)
	if (not check):
		notEnoughBillsNotification()
	hardwareDispense(bills)
	markDispensed(rtime)
	subtractBills(bills)
	dispensedNotification()
	checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
	timerThread.start()
	data.waitForDispense = False

def updateTimeLCD (rTime):
	print 'lcd time'
	print rTime
	#print rTime on LCD 'remaining time to next medication'
	
def hardwareDispense(rBills):
	print 'hardwareDispense Called'
	#dispense this array
	
def openDoor():
	print 'openDoor Called'
	#hardware openDoor
	timerThread.cancel()
	doorOpenedNotification()

def openWarehouse():
	print 'openWarehouse Called'
	#hardware openWarehouse
	warehouseOpenedNotification()

def callEmergencyNotification():
	emergencyNotification()

def restartRPI():
	subprocess.Popen("sudo ./restart.sh", shell=False)

#returns measurements from sensors temperature, light
def getSensorData():
	return "50","70"

#accepts boolean state, turn on/off switches
def updateSwitch(state1, state2):
	print "switch 1,2 should be" + state1 + ", " + state2
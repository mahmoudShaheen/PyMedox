#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				   Control Hardware						#
#################################

#########################
#serial codes								#
#	hardwareDispense: h; 1; 2; 3; 4	#
#	openDoor: d;							#
#	openWarehouse: w;					#
#	getSensorData: s;					#
#########################

from pythonSQL import *
from notification import *
from billCount import *
from arduino import *
from pinout import *
import data
import time #for time.sleep

import subprocess #for calling restart shell script

import threading #for timer thread
import datetime #for datetime.timedelta
doorDelay = 5*60 #5 minutes then send door not opened notification
timerThread = threading.Timer(doorDelay, doorNotOpenedNotification) #to check if door not opened for 5 minutes

def dispenseBills(rTime):
	print 'dispensing Bills Called'
	data.waitForDispense = True
	bills = getBills(rTime)
	check = checkBills(bills)
	if (not check): #no enough pills for this schedule
		notEnoughBillsNotification()
		print "no enough pills for this schedule"
		data.waitForDispense = False
		data.emptyWarehouse = True
		return
	hardwareDispense(bills)
	markDispensed(rTime)
	subtractBills(bills)
	dispensedNotification()
	checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
	try:
		timerThread.cancel()
	except:
		print "trying to cancel not started thread: doorThread"
	try:
		timerThread = threading.Timer(doorDelay, doorNotOpenedNotification) #to check if door not opened for 5 minutes
		timerThread.start()
	except:
		print "door thread at dispenseBills Exception"
	data.waitForDispense = False

def updateTimeLCD (rTime):
	#print 'lcd time'
	#print rTime
	#print rTime on LCD 'remaining time to next medication'
	return
	
def hardwareDispense(rBills):
	print 'hardwareDispense Called for ' + str(rBills[0]) + ", "  + str(rBills[1]) + ", "  + str(rBills[2]) + ", " + str(rBills[3])  
	while (data.waitForSerial):
		time.sleep(data.serialDelay)
	data.waitForSerial = True
	#dispense this array
	sendSerial("h")
	sendSerial(str(rBills[0]))
	sendSerial(str(rBills[1]))
	sendSerial(str(rBills[2]))
	sendSerial(str(rBills[3]))
	state = getSerial()
	if (state == "t"):
		print 'dispense ended successfully'
	if (state == "f"):
		print 'dispense ended with errors'
	data.waitForSerial = False
	
def openDoor():
	print 'openDoor Called'
	try:
		timerThread.cancel()
	except:
		print "trying to cancel not started thread: doorThread"
	while (data.waitForSerial):
		time.sleep(data.serialDelay)
	data.waitForSerial = True
	#hardware openDoor
	sendSerial("d")
	data.waitForSerial = False
	timerThread.cancel()
	doorOpenedNotification()

def openWarehouse():
	print 'openWarehouse Called'
	while (data.waitForSerial):
		time.sleep(data.serialDelay)
	data.waitForSerial = True
	#hardware openWarehouse
	sendSerial("w")
	data.waitForSerial = False
	warehouseOpenedNotification()

#returns measurements from sensors temperature, light
def getSensorData():
	#if(data.waitForSerial):
	#	return False, False
	#sendSerial("s")
	#temp = getSerial()
	#light = getSerial()
	#return temp, light
	return "100", "100"

#accepts boolean state, turn on/off switches
def updateSwitch(state1, state2, state3, state4, state5, state6, state7, state8):
	print "switches should be " + str(state1) + ", " +  str(state2)  + ", " +  str(state3)  + ", " +  str(state4)  + ", " +  str(state5)  + ", " +  str(state6)  + ", " +  str(state7)  + ", " +  str(state8) 
	gpioSwitches(state1, state2, state3, state4, state5, state6, state7, state8)

def callEmergencyNotification():
	emergencyNotification()

def restartRPI():
	subprocess.Popen("sudo ./restart.sh", shell=False)

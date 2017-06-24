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
import data
import time #for time.sleep

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
	#print 'lcd time'
	#print rTime
	#print rTime on LCD 'remaining time to next medication'
	return
	
def hardwareDispense(rBills):
	print 'hardwareDispense Called'
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
	data.waitForSerial = False
	if (state == "t"):
		print 'dispense ended successfully'
	if (state == "f"):
		print 'dispense ended with errors'
	
def openDoor():
	print 'openDoor Called'
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
	if(data.waitForSerial):
		return False, False
	sendSerial("s")
	temp = getSerial()
	light = getSerial()
	return temp, light

#accepts boolean state, turn on/off switches
def updateSwitch(state1, state2):
	print "switch 1,2 should be" + state1 + ", " + state2
	#TODO: RPI GPIO to 8 led matrix

def callEmergencyNotification():
	emergencyNotification()

def restartRPI():
	subprocess.Popen("sudo ./restart.sh", shell=False)

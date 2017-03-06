#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				   Control Hardware							#
 ###########################################################

from pythonSQL import *
from notification import *
import data

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
	doorOpenedNotification()

def openWarehouse():
	print 'openWarehouse Called'
	#hardware openWarehouse
	warehouseOpenedNotification()

def callEmergencyNotification():
	emergencyNotification()

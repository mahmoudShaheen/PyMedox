#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  	     Bill Count							#
#################################

#bill count monitoring, updating

from pythonSQL import getTotalDayBills, checkBills
from notification import notEnoughDayBillsNotification
import firebase
import data

#checks if bills in warehouse are enough for one day, also updates bill count in fb db
#if not sends notification to care giver
def checkDay():
	totalBills = getTotalDayBills()
	enough = checkBills(totalBills)
	if (not enough):
		notEnoughDayBillsNotification()
		updateStatus("fail")
	if(enough)
		updateStatus("ok")
	updateBillCount() #update bill count in firebase database

#updates bill count in firebase database
def updateBillCount():
	execCommand("getBillCount")

def updateStatus(state):
	stateJson = "{ bills :" + state + "}"
	firebase.patch(data.stateURL, stateJson)
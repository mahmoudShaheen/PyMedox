#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  	     Bill Count							#
#################################

#bill count monitoring, updating

from pythonSQL import getTotalDayBills, checkBills, getBillCount
from notification import notEnoughDayBillsNotification

import firebase
import data
import json

#checks if bills in warehouse are enough for one day, also updates bill count in fb db
#if not sends notification to care giver
def checkDay():
	totalBills = getTotalDayBills()
	enough = checkBills(totalBills)
	if (not enough):
		notEnoughDayBillsNotification()
		updateStatus("fail")
	if(enough):
		updateStatus("ok")
	updateBillCount() #update bill count in firebase database

#updates bill count in firebase database
#the same as execCommand("getBillCount")
#but can't import command module due to circular dependent imports
def updateBillCount():
	billCount = getBillCount()
	billCountJson = "{ \"billCount\" :\"" + billCount + "\"}"
	billCountJson = json.loads(billCountJson)
	firebase.patch(data.dataURL, billCountJson)

def updateStatus(state):
	stateJson = "{ \"bills\" :\"" + state + "\"}"
	stateJson = json.loads(stateJson)
	firebase.patch(data.stateURL, stateJson)
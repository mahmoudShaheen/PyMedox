#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  	     Bill Count							#
#################################

#bill count monitoring, updating

from pythonSQL import getTotalDayBills, checkBills
from notification import notEnoughDayBillsNotification

#checks if bills in warehouse are enough for one day, also updates bill count in fb db
#if not sends notification to care giver
def checkDay():
	totalBills = getTotalDayBills()
	enough = checkBills(totalBills)
	if (not enough):
		notEnoughDayBillsNotification()
	updateBillCount() #update bill count in firebase database

#updates bill count in firebase database
def updateBillCount():
	execCommand("getBillCount")
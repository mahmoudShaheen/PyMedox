#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  		  Sync								#
 ###########################################################

from pythonSQL import *
import time
import data
 
#check database if there is update
#auto run in background and updates a variables in data
#main uses these variables to take an action

def syncStart():
	print 'sync thread called i\'m inside'
	while True:
		warehouseStatus = statusWarehouseCheck()
		commandStatus = statusCommandCheck()
		if (warehouseStatus == '1'):
			data.scheduleChanged = True
		
		if (commandStatus == '1'):
			data.avaliableCommand = True
		
		print 'still inside sync'
		time.sleep(syncDelay) #delay to avoid errors
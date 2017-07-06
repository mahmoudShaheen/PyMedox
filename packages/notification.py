#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  	  Notifications							#
#################################

###############
#notificationLevel: 	#
#	0 info 				#
#	1 Emergency		#
###############

#to send notifications through Firebase 
import data
import firebase
import time
	
#to watch to open drawer
def dispensedNotification():
	message = "Medications Dispensed Successfully!"
	level = 0
	receiver = "watch"
	sendNotification(message, level, receiver)

##########
#to mobile#
##########
def doorOpenedNotification():
	message = "Drawer opened!"
	level = 0
	receiver = "mobile"
	sendNotification(message, level, receiver)
	
def doorNotOpenedNotification():
	message = "Drawer NOT opened!"
	level = 1
	receiver = "mobile"
	sendNotification(message, level, receiver)


def warehouseOpenedNotification():
	message = "warehouse opened!"
	level = 1
	receiver = "mobile"
	sendNotification(message, level, receiver)

def notEnoughBillsNotification():
	message = "No enough Pills!"
	level = 1
	receiver = "mobile"
	sendNotification(message, level, receiver)
	
def notEnoughDayBillsNotification():
	message = "Pills aren't enough for one day'!"
	level = 1
	receiver = "mobile"
	sendNotification(message, level, receiver)

def emergencyNotification():
	message = "emergency"
	level = 1
	receiver = "mobile"
	sendNotification(message, level, receiver)
 
 #send notification to database and update notification status by call statusNotificationUpdate
def sendNotification(rMessage, rLevel, rReceiver):
	#Initialize 
	title = "message from Box"
	#time format
	#jul 06, 2017 08:05:01 PM to jul 6, 2017 8:05:01 PM
	now = time.strftime("%b %d, %Y %I:%M:%S %p")
	if(now[13] == "0"):
		now = now[:13] + now[14:]
	if(now[4] == "0"):
		now = now[:4] + now[5:]
	
	#creating JSON object
	message = {}
	message["message"]= rMessage
	message["title"] = title
	message["time"] = now
	message["level"] = str(rLevel)
	message["to"] = rReceiver 
	
	#Send message to database for cloud function to deliver
	firebase.push(data.messagesURL, message)
	
	time.sleep(data.notificationDelay) #delay to avoid errors

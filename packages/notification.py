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
	
#to watch to open drawer
def dispensedNotification():
	message = "Medications Dispensed Successfully!"
	level = 0
	receiver = "watch"
	sendNotification(message, level, receiver)

##########
#to phone#
##########
def doorOpenedNotification():
	message = "Drawer opened!"
	level = 0
	receiver = "phone"
	sendNotification(message, level, receiver)
	
def doorNotOpenedNotification():
	message = "Drawer NOT opened!"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)


def warehouseOpenedNotification():
	message = "warehouse opened!"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)

def notEnoughBillsNotification():
	message = "No enough Bills!"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)
	
def notEnoughDayBillsNotification():
	message = "Bills aren't enough for one day'!"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)

def emergencyNotification():
	message = "emergency"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)
 
 #send notification to database and update notification status by call statusNotificationUpdate
def sendNotification(rMessage, rLevel, rReceiver):
	#Initialize 
	title = "message from Box"
	
	#creating JSON object
	message = "{"
	message += "message : " + rMessage + ", "
	message += "title : " + title + ", "
	message += "level : " + str(rLevel) + ", "
	message += "to : " + rReceiver 
	message += "}"
	
	#Send message to database for cloud function to deliver
	firebase.push(data.messagesURL, message)
	
	time.sleep(data.notificationDelay) #delay to avoid errors

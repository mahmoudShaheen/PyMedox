#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  	  Notifications							#
 ###########################################################

#####################
#notificationLevel: #
#	0 low 			#
#	1 High 			#
#	2 Emergency		#
#	5 data			#
#####################

#to send notifications through Firebase 
from pyfcm import FCMNotification
import data
	
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

def warehouseOpenedNotification():
	message = "warehouse opened!"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)

def billCountNotification(billCount):
	message = billCount
	level = 5
	receiver = "phone"
	sendNotification(message, level, receiver)

def notEnoughBillsNotification():
	message = "No enough Bills!"
	level = 1
	receiver = "phone"
	sendNotification(message, level, receiver)

def emergencyNotification():
	message = "emergency"
	level = 2
	receiver = "phone"
	sendNotification(message, level, receiver)
 
 #send notification to database and update notification status by call statusNotificationUpdate
def sendNotification(rMessage, rLevel, rReceiver):
	#Initialize 
	push_service = FCMNotification(api_key = data.serverKey)
	
	if rReceiver == "watch": #send notification to watch
		registration_id = data.watchToken
		message_title = str(rLevel)
		message_body = rMessage
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		print result
	
	if rReceiver == "phone": #send notification to phone
		registration_id = data.mobileToken
		message_title = str(rLevel)
		message_body = rMessage
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
		print result
	
	time.sleep(data.notificationDelay) #delay to avoid errors

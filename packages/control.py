#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  		  Control								#
 ###########################################################

#to send sensors data to fb db 
#also changes switches states if changed in db


from controlHardware import *

import threading #to send data to fb db every n seconds

import json
import StringIO
import unicodedata
import firebase
import data

def getValues(): #called when prog start, connectivity returns, subscribe event
	rcvData = firebase.get(data.commandURL) #get switches states from FDB
	if rcvData is not None: #if the class is empty the parsed data is None
		io = StringIO
		states = json.dumps(rcvData, io) #convert data to string instead of list
		states = states[1:-1] #removes [] from data

		switch1 = temp.get('switch1') #get value by key
		uncoded1 = unicodedata.normalize('NFKD', switch1).encode('ascii','ignore')
		state1 = (uncoded1 == "on") #whether switch should be on or not
		switch2 = temp.get('switch2') #get value by key
		uncoded2 = unicodedata.normalize('NFKD', switch2).encode('ascii','ignore')
		state2 = (uncoded2 == "on") #whether switch should be on or not
			
		updateSwitch(state1, state2) #updates switches states

def controlStart():
	S = firebase.subscriber(data.switchURL, getValues)  #when command class changes in FDB it calls getCommand
	S.start()  #start the subscriber

def sendSensorDataStart():
	threading.Timer(data.sensorDelay, sendSensorDataStart).start()
	temperature, light = getSensorData()
	temperatureJson = "{ temperature :" + temperature + "}"
	firebase.patch(data.sensorURL, temperatureJson)
	lightJson = "{ light :" + light + "}"
	firebase.patch(data.sensorURL, lightJson)

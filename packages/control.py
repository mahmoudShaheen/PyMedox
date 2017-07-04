#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  		  Control								#
#################################

#to send sensors data to fb db 
#also changes switches states if changed in db


from controlHardware import *

import threading #to send data to fb db every n seconds

import json
import firebase
import data

def getValues(args): #called when prog start, connectivity returns, subscribe event
	states = firebase.get(data.switchURL) #get switches states from FDB
	if states is not None: #if the class is empty the parsed data is None

		switch1 = states['switch1'] #get value by key
		state1 = (switch1 == "on") #whether switch should be on or not
		
		switch2 = states['switch2'] #get value by key
		state2 = (switch2 == "on") #whether switch should be on or not
		
		switch3 = states['switch3'] #get value by key
		state3 = (switch3 == "on") #whether switch should be on or not
		
		switch4 = states['switch4'] #get value by key
		state4 = (switch4 == "on") #whether switch should be on or not
		
		switch5 = states['switch5'] #get value by key
		state5 = (switch5 == "on") #whether switch should be on or not
		
		switch6 = states['switch6'] #get value by key
		state6 = (switch6 == "on") #whether switch should be on or not
		
		switch7 = states['switch7'] #get value by key
		state7 = (switch7 == "on") #whether switch should be on or not
		
		switch8 = states['switch8'] #get value by key
		state8 = (switch8 == "on") #whether switch should be on or not
		
		updateSwitch(state1, state2, state3, state4, state5, state6, state7, state8) #updates switches states

def controlStart():
	S = firebase.subscriber(data.switchURL, getValues)  #when command class changes in FDB it calls getCommand
	S.start()  #start the subscriber

def sendSensorDataStart():
	threading.Timer(data.sensorDelay, sendSensorDataStart).start()
	temperature, light = getSensorData()
	if (temperature == False or light == False): #Refused as serial channel is used
		return
	temperatureJson = "{\"temperature\" :\"" + temperature + "\"}"
	temperatureJson = json.loads(temperatureJson)
	firebase.patch(data.sensorURL, temperatureJson)
	lightJson = "{\"light\" :\"" + light + "\"}"
	lightJson = json.loads(lightJson)
	firebase.patch(data.sensorURL, lightJson)

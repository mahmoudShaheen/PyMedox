#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  	  	Commands							#
 ###########################################################

#to receive commands and execute them

from controlHardware import *
import json
import StringIO
import unicodedata
import firebase
import data

def execCommand(rCommand): #each command in the array should be "command,arg1,arg2,..."
	for row in rCommand:
		commandList = rCommand.split(",")
		command = commandList.pop(0)
		
		#No Switch in python
		if (command == "openDoor"): #openDoor
			openDoor()
		
		if(command == "dispenseNext"): #dispense next now
			data.schedulerCheck == True #tells main that the scheduler timer has finished so it dispense next
		
		if(command[0] == "dispense"): #dispense drugs
			billsArray = [int(i) for i in r]
			hardwareDispense(billsArray)
			openDoor()

def getCommand(): #called when prog start, connectivity returns, subscribe event
	rcvData = firebase.get(data.commandURL) #get commands from FDB
	if rcvData is not None: #if the class is empty the parsed data is None
		data.waitForCmd = True
		firebase.put(data.commandURL, {}) #delete commands after parsing
		io = StringIO
		commands = json.dumps(jsonData, io) #convert data to string instead of list
		commands = commands[1:-1] #removes [] from data
		commands = commands.split(', {') #split string to JSON objects style #JSON.loads accepts only one object at a time
		commandArray = []
		for row in commands:
			temp = json.loads('{' + row) #create JSON object
			cmd = temp.get('cmd') #get value by key
			uncoded = unicodedata.normalize('NFKD', cmd).encode('ascii','ignore')
			commandArray.append(uncoded) #the returned value is Unicode 
		execCommand(commandArray) #execute the commands "sends array of parsed commands"
	data.waitForCmd = False

def commandStart():
	S = firebase.subscriber(data.commandURL, getCommand)  #when command class changes in FDB it calls getCommand
	S.start()  #start the subscriber
	
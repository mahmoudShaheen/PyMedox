#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				  	  	Commands							#
#################################

#to receive commands and execute them

from controlHardware import *
from pythonSQL import *
from sync import *
from notification import *
from billCount import checkDay

import json
import firebase
import data

def execCommand(rCommand): #each command in the array should be "command,arg1,arg2,..."
	commandList = rCommand.split(",")
	command = commandList.pop(0)
	
	#No Switch in python
	if (command == "openDoor"): #openDoor
		openDoor()
	
	if(command == "openWarehouse"): #open warehouse
		openWarehouse()
	
	if(command == "dispenseNext"): #dispense next now
		data.schedulerCheck == True #tells main that the scheduler timer has finished so it dispense next
	
	if(command == "dispense"): #dispense drugs
		billsArray = [int(i) for i in commandList]
		hardwareDispense(billsArray)
		openDoor()
		checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
	
	if(command == "clearTimetable"): #empty the timetable
		clearTimetable()
	
	if(command == "clearBills"): #reset bill count to zeros
		clearBills()
	
	if(command == "addBills"): #add received bill count to original count
		billsArray = [int(i) for i in commandList]
		print billsArray
		addBills(billsArray)
		checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
	
	if(command == "forceUpdateTimetable"): #force update timetable
		syncdb()
		checkDay() #checks if bills in warehouse are enough for one day, also updates bill count in fb db
	
	if(command == "getBillCount"): #send saved bill count from RPI to phone
		billCount = getBillCount()
		billCountJson = "{ \"billCount\" :\"" + billCount + "\"}"
		billCountJson = json.loads(billCountJson)
		firebase.patch(data.dataURL, billCountJson)
	
	if(command == "restartRPI"):
		restartRPI()
		
def getCommand(args): #called when prog start, connectivity returns, subscribe event
	commands = firebase.get(data.commandURL) #get commands from FDB
	if commands is not None: #if the class is empty the parsed data is None
		data.waitForCmd = True
		firebase.put(data.commandURL, {}) #delete commands after parsing
		for key, value in commands.iteritems():
			cmd = str(value['cmd'])
			print cmd
			execCommand(cmd) #execute the commands "sends array of parsed commands"
		data.waitForCmd = False

def commandStart():
	S = firebase.subscriber(data.commandURL, getCommand)  #when command class changes in FDB it calls getCommand
	S.start()  #start the subscriber


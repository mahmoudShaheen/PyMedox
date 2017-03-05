#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  	  	Commands							#
 ###########################################################

#to execute commands from database

from controlHardware import *
from pythonSQL import *

def commandStart():
	commands = getCommands()
	if not (commands is None):
		for row in commands:
			command = row[0]
			execCommand(command)
		
def execCommand(rCommand): #command should be "command,arg1,arg2,..."
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

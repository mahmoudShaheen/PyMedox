#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				 		  Data								#
#################################

#hold some data and statics for the program
#can be accessed from all modules
#used also to sync threads


#Enumerators
warehouseCount = 4
#Delay
notificationDelay = 2
syncDelay = 10
osDelay = 1000
mainLoopDelay = 1 #can't be more as it does other work like updateLCD
sensorDelay = 10 #update sensor values in db every 10 seconds
serialDelay = 1 #wait another operation on serial port to finish

#SQLite database
dbName = "../box.db"

#threads synchronization
schedulerCheck = False #to check if the scheduler finishes
scheduleChanged = True #to stop the tread 'scheduler' and start again if user changed the schedule or dispense completed
emptyTimetable = False #check if the table is empty
waitForDispense = False #to stop scheduler until dispensing process finishes "added to complete other tasks while dispensing process is running"
schedulerAlive = False #is_alive isn't working

waitForSync = False #to stop main until db is updated
waitForCmd = False #to stop main until commands are executed
waitForSerial = False #to make one serial operation at time

###Arduino Serial Port
#rootpath = "/dev/serial/by-id/"
#arduinoPort = rootpath + "usb-Arduino__www.arduino.cc__0043_95333303031351F08082-if00" #get arduino port using "ls /dev/serial/by-id"
arduinoPort = "/dev/ttyACM0" #will mostly work fine
baudRate = 9600

###GPIO Pins
switch1 = 2
switch2 = 3
switch3 = 4
switch4 = 17
switch5 = 27
switch6 = 22
switch7 = 10
switch8 = 9

###Firebase real-time database paths
rootURL = "medox-f7251.firebaseio.com"
UID = "Vbxp1DKBbMckkknNyDW0c0IGEYa2"
userURL = rootURL + "/users/" + UID
messagesURL = userURL + "/notification/.json"
commandURL = userURL + "/command/" + ".json"
sensorURL = userURL + "/iot/sensor/" + ".json"
switchURL = userURL + "/iot/switch/" + ".json"
timetableURL = userURL + "/timetable/" + ".json"
warehouseURL = userURL + "/warehouse/" + ".json"
dataURL = userURL + "/data/" + ".json"
configURL = userURL + "/config/" + ".json"
stateURL = userURL + "/status/" + ".json"

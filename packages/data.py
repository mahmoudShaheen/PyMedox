#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				 		  Data								#
 ###########################################################

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


###Tokens
#mobile token
mobileToken = ""
#watch token
watchToken = ""

###Firebase real-time database paths
rootURL = "medox-f7251.firebaseio.com"
messagesURL = rootURL + "/messages/.json"
UID = "Vbxp1DKBbMckkknNyDW0c0IGEYa2"
userURL = rootURL + "/users/" + UID
commandURL = userURL + "/command/" + ".json"
timetableURL = userURL + "/timetable/" + ".json"
warehouseURL = userURL + "/warehouse/" + ".json"
tokenURL = userURL + "/token/" + ".json"
billCountURL = userURL + "/data/billCount/" + ".json"
configURL = userURL + "/config/" + ".json"

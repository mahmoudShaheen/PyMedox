#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				 		  Data								#
 ###########################################################

#hold some data and statics for the program
#can be accessed from all modules
#used also for sync threads


#Enumerators
warehouseCount = 4
#Delay
notificationDelay = 2
syncDelay = 10
osDelay = 1000
mainLoopDelay = 1 #can't be more as it does other work like updateLCD

#SQLite database
dbName = "box.db"

#threads synchronization
schedulerCheck = False #to check if the scheduler finishes
scheduleChanged = True #to stop the tread 'scheduler' and start again if user changed the schedule or dispense completed
emptyTimetable = False #check if the table is empty
waitForDispense = False #to stop scheduler until dispensing process finishes "added to complete other tasks while dispensing process is running"

schedulerAlive = False #is_alive isn't working


###Firebase Keys
# Your API-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudMessaging
#sender ID not used
senderID = "108587114762" 
#Legacy Server key can be used but not recommended
legacyServerkey = "AIzaSyDSYqjLbeHaKPcMg_kGai54MgDmeTCV-XI"
#Server key used to send messages
serverkey = "AAAAGUhL4Qo:APA91bFMS9HI801s8Zy5eHKBqnD2R-nUBbknoufW0DG-gBtnGaCEjsS9munlsVpWNfTowIxIRUfHa59hS8TT7Ygej2biL1dPvncEx4rzxuBsm8rrOESW7AbMUtLHzuV1rbgihUFryj3i"
#mobile token
mobileToken = "eWf4a1ANSGQ:APA91bEDXv2TRe0RR2i1ecKjuyhv7xv4_ly0E6c7uwd5FFuOS02VNl-Qno8veyaKVG3t_5PolZXeJkwDxe9S7XmkI-QLov4NNstPLl-VZe3z4W1MZ0l05_nCw9A-ruXjzJFGDwJLWFwH"
#watch token
watchToken = ""

###Firebase real-time database paths
rootURL = "pytest-3452a.firebaseio.com/.json"
commandURL = "pytest-3452a.firebaseio.com/command/.json"
timetableURL = "pytest-3452a.firebaseio.com/timetable/.json"
warehouseURL = "pytest-3452a.firebaseio.com/warehouse/.json"

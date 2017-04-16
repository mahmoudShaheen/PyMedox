#!/usr/bin/env python

#############################################################
#				@author: Mahmoud Shaheen					#
#				 MedicalBox IOT Project						#
#				  		  tokens								#
 ###########################################################

#to receive changes in tokens 'mobile & watch'

import data
import firebase

def updateToken():
	rcvData = firebase.get(data.tokenURL) #get timetable from FDB
	if rcvData is not None: #if the class is empty the parsed data is None
		io = StringIO
		tokens = json.dumps(rcvData, io) #convert data to string instead of list
		tokens = tokens[1:-1] #removes [] from data

		time = temp.get('mobile') #get value by key
		uncodedMobile = unicodedata.normalize('NFKD', time).encode('ascii','ignore')
		data.mobileToken = uncodedMobile #the returned value is Unicode 
		drug = temp.get('watch') #get value by key
		uncodedWatch = unicodedata.normalize('NFKD', drug).encode('ascii','ignore')
		data.watchToken = uncodedWatch #the returned value is Unicode 


def tokenStart():
	S = firebase.subscriber(data.tokenURL, updateToken)  #when timetable class changes in FDB it calls syncNow
	S.start()  #start the subscriber

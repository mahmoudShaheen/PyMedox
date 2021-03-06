#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				   			Arduino							#
#################################

#functions for serial communication with Arduino
#called from controlHardware module

import serial
import data
import time

ser = serial.Serial(data.arduinoPort)
ser.baudrate = data.baudRate
time.sleep(5) #wait for serial communication to start

#encodes string and sends it on serial port for Arduino
def sendSerial(serialString): #checks if the port is closed to re-open it
	if(not ser.isOpen):
		ser.open()
		time.sleep(5)
	serialString = str(serialString) #makes sure that the data is string "convert any to string"
	serialString = serialString.encode() #encodes the string "converts string to byte array"
	print "serial to write:  " + serialString
	ser.write(serialString)

#gets a line from serial port from Arduino
def getSerial():
	if(not ser.isOpen): #checks if the port is closed to re-open it
		ser.open()
		time.sleep(5)
	line = ser.readline() #get a line from serial terminated by \n
	line = line.strip() #removers \r\n at the end of the string
	line = line.decode("utf-8")  #removes b at the start of the string "converts byte to string"
	print "serial received: ", line
	return line

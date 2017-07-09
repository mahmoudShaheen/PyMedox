#!/usr/bin/env python

#################################
#				@author: Mahmoud Shaheen			#
#				 MedicalBox IOT Project				#
#				   			Pinout							#
#################################

#for controlling GPIO

import data

import RPi.GPIO as GPIO           # import RPi.GPIO module
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD
GPIO.setwarnings(False)
set a pins as an output
GPIO.setup(data.switch1, GPIO.OUT)
GPIO.setup(data.switch2, GPIO.OUT)
GPIO.setup(data.switch3, GPIO.OUT)
GPIO.setup(data.switch4, GPIO.OUT)
GPIO.setup(data.switch5, GPIO.OUT)
GPIO.setup(data.switch6, GPIO.OUT)
GPIO.setup(data.switch7, GPIO.OUT)
GPIO.setup(data.switch8, GPIO.OUT)



def gpioSwitches(state1, state2, state3, state4, state5, state6, state7, state8):
	GPIO.output(data.switch1, state1)       # set pin value to switch state
	GPIO.output(data.switch2, state2)       # set pin value to switch state
	GPIO.output(data.switch3, state3)       # set pin value to switch state
	GPIO.output(data.switch4, state4)       # set pin value to switch state
	GPIO.output(data.switch5, state5)       # set pin value to switch state
	GPIO.output(data.switch6, state6)       # set pin value to switch state
	GPIO.output(data.switch7, state7)       # set pin value to switch state
	GPIO.output(data.switch8, state8)       # set pin value to switch state
	print "gpio should be " + str(state1) + ", " +  str(state2)  + ", " +  str(state3)  + ", " +  str(state4)  + ", " +  str(state5)  + ", " +  str(state6)  + ", " +  str(state7)  + ", " +  str(state8) 
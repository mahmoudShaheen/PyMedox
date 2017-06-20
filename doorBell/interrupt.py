#!/usr/bin/env python 

import time
import subprocess
import RPi.GPIO as GPIO

def interruptCallBack():
	print "call back called"
	subprocess.Popen("sudo ./cam.sh", shell=True)
	time.sleep(3)
	
def interruptCatcher():
	print "interruptCatcher Called"
	GPIO.setmode(GPIO.BCM)
	# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
	GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
	while True:
		print "Waiting for rising edge on port 4"  
		GPIO.wait_for_edge(4, GPIO.RISING)  
		print "Rising edge detected on port 4. Calling function" 
		interruptCallBack()

def callInterruptCatcher():
	print "callInterruptCatcher called"
	interruptThread = threading.Thread(target=interruptCatcher)
	interruptThread.start()
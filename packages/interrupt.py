#!/usr/bin/env python2.7  

import time
import subprocess
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def interruptCallBack():
	print "call back called"
	subprocess.Popen("sudo ./cam.sh", shell=True)
	time.sleep(3)
	

# GPIO 24 set up as an input, pulled down, connected to 3V3 on button press  
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
while True:
	try:  
		print "Waiting for rising edge on port 4"  
		GPIO.wait_for_edge(4, GPIO.RISING)  
		print "Rising edge detected on port 4. Calling function" 
		interruptCallBack()
	  
	except KeyboardInterrupt:  
		GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  

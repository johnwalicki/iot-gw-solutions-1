##*****************************************************************************
## Copyright (c) 2014 IBM Corporation and other Contributors.
##
## All rights reserved. This program and the accompanying materials
## are made available under the terms of the Eclipse Public License v1.0
## which accompanies this distribution, and is available at
## http://www.eclipse.org/legal/epl-v10.html
##
## Contributors:
## IBM - Initial Contribution
##*****************************************************************************
## IoT Foundation QuickStart Driver
## A sample IBM Internet of Things Foundation Service client for Intel Internet of Things Gateway Solutions

import time
import json
import uuid
import ibmiotf
import ibmiotf.device
from time import sleep
import signal
import sys


#Class for retrieving CPU % utilisation
class CPUutil(object):
		def __init__(self):
				self.prev_idle = 0
				self.prev_total = 0
				self.new_idle = 0
				self.new_total = 0
		def get(self):
				self.read()
				delta_idle = self.new_idle - self.prev_idle
				delta_total = self.new_total - self.prev_total
				cpuut = 0.0
				if (self.prev_total != 0) and (delta_total != 0):
						cpuut = ((delta_total - delta_idle) * 100.0 / delta_total)
				return cpuut
		def read(self):
				self.prev_idle = self.new_idle
				self.prev_total = self.new_total
				self.new_idle = 0;
				self.new_total = 0;
				with open('/proc/stat') as f:
						line = f.readline()
				parts = line.split()
				if len(parts) >= 5:
						self.new_idle = int(parts[4])
						for part in parts[1:]:
								self.new_total += int(part)


#Initialise class to retrieve CPU Usage
cpuutil = CPUutil()

macAddress = hex(uuid.getnode())[2:-1]
macAddress = format(long(macAddress, 16),'012x')
#Remind the user of the mac address further down in code (post 'connecting to WIoTP')

#Share the name of the Configuration File to connect to the WIoTP as a Registered Device
deviceFile="device.cfg"

# Set a parameter that helps differentiate the connection to WIoTP, either as a Registered or as a QuickStart service
fileFound=""

#Set the values for variables to connect to the WIoTP using Quickstart service
organization = "quickstart"
deviceType = "iotsample-gateway"
deviceId = macAddress
broker = ""
topic = "iot-2/evt/status/fmt/json"
username = ""
password = ""

#Raise exception, if the contents do not exist
error_to_catch = getattr(__builtins__,'FileNotFoundError', IOError)

#The following code snippet looks for the Config file in the `pwd`
#Tries to open the Config file and read through the values of the configuration parameters
#If it doesn't find the Config file, it then switches to connect to the Platform using QuickStart service

try:

		#file_object = open("device.cfg")
		file_object = open(deviceFile)
		
		for line in file_object:
				
				readType, readValue = line.split("=")
			
				if readType == "org":	
						organization = readValue.strip()
				elif readType == "type": 
						deviceType = readValue.strip()
				elif readType == "id": 
						macAddress = readValue.strip()
				elif readType == "auth-method": 
						username = "use-token-auth"
				elif readType == "auth-token": 
						password = readValue.strip()
				else:
						print("please check the format of your config file") #will want to repeat this error further down if their connection fails?
		
		file_object.close()
		fileFound = "true"
		print("Configuration file found - connecting to the registered service")
		
except error_to_catch:
		print("No config file found, connecting to the Quickstart service")
		print("MAC address: " + macAddress)
		fileFound = "false"


#Creating the client connection
#Set clientID and broker
clientID = "d:" + organization + ":" + deviceType + ":" + macAddress
broker = organization + ".messaging.internetofthings.ibmcloud.com"

# Define a method that helps publish the event(s) at every 5 second interval
def eventLoop():
#	       while true:
		 	cpuutilvalue = cpuutil.get()
		      	print cpuutilvalue

                	# msg = json.JSONEncoder().encode({"d":{"cpuutil":cpuutilvalue}})

                	msg = {"d":{"cpuutil":cpuutilvalue}}

                	deviceClient.publishEvent("cpuUtil","json", msg, qos=0)
                	print "message published"

                	time.sleep(5)
			pass

# Define a method that sets the Username and Password, while initiating the connection using QuickStart Service
def username_pw_set(self, username, password=None):
		self._username = username.encode('utf-8')
        	self._password = password

# 'fileFound' is set to 'true', if the Config file is located within the `pwd`
if fileFound == "true":
		options = ibmiotf.device.ParseConfigFile(deviceFile)
		deviceClient = ibmiotf.device.Client(options)
		#print("(Press Ctrl+C to disconnect)")
		deviceClient.connect()
		
		while 0 == 0:
				eventLoop()
# The 'else' condition is invoked, if the code fails to find a Config file, kickstarting connection using QuickStart service
else:
				options = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": username, "auth-token": password}
				deviceClient = ibmiotf.device.Client(options)
				deviceClient.connect()
				while 0 == 0:
						eventLoop()
#Marking the completion of the Program here
print("Connection Process Completed Successfully")

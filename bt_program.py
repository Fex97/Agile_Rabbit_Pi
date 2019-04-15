import bluetooth
#import serial
#import logging
#import time
#import os
#ser = serial.Serial('/dev/ttyAMA0',9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)

#logging.basicConfig(filename='startup.log', filemode='w', format='%(message)s')

print ("BLUETOOTHCTL PROGRAM...\n\r")

nearby_devices = bluetooth.discover_devices()
print(nearby_devices)

while True:
	print("hjsh")
#logging.error("LATEST STARTUP LOG")
num=0
time=0
device_list = []
def switch_cmd(num):
   	 switcher = {
    	0: "bluetoothctl\r",
    	1: "scan on\r",
    	}
	return switcher.get(num)
    
for x in range(3):
	cmd = switch_cmd(num)
	print(cmd)
    	ser.write(str(cmd))
    	#logging.error("request at cmd: " + str(cmd))
	print("TEST")
    	while True:
		print("EHILE")
        	response = ser.readline()
		print(response)
        	if num == 0:
        		num=1;
			break
        	if "[NEW]" in response:
            		print(response)
            		device_list.append(response)
            		time=0
        	if device_list >= 100:
            		print("BATCH OF DEVICES FOUND CONNECT FIREBASE")

        	else:
            		time = time +1
        	if time >= 200000:
            		print("TIMEOUT. CONNECT TO FIREBASE ANYWAY")

        
            

     



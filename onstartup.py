import serial
import logging
import time
import os
from firebase import firebase
firebase=firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)
ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)

logging.basicConfig(filename='startup.log', filemode='w', format='%(message)s')

print ("STARTUP RABBIT_PI GSM module...\n\r")
logging.error("LATEST STARTUP LOG")
num=0
last_cmd=7
fail=0
okay=0
totalfailure=0
runonce = 0
def switch_cmd(num):
    switcher = {
    0: "AT\r",
    1: "AT+CGNSPWR=1\r",
    2: "AT+CGNSPWR?\r",
    3: "AT+COPS?\r",
    4: "AT+CSQ\r",
    5: "AT+CBC\r",
    6: "AT+CGNSINF\r",
    }
    return switcher.get(num)
    
for x in range(last_cmd):
    cmd = switch_cmd(num)
    ser.write(str(cmd))
    runonce=0
    print("REQUEST: " + str(cmd))
    logging.error("request at cmd: " + str(cmd))
    while True:
        response = ser.readline()
        if "+" in response and not cmd in response:
        	if num == 2 and runonce == 0:
        		tempSplit = response.split(":")
                	if tempSplit == 0:
                        	print("GNSS IS OFF")
                        	logging.error("GNSS IS OFF")
                    	else:
                        	okay = okay+1
                        	print("GNSS IS ON")
                        	logging.error("GNSS IS ON")
                	runonce=1

            	if num == 3 and runonce == 0:
            		#NEED TO BE CHECKED
                	print ("NETWORK " + response)
                	logging.error("NETWORK " +response)
                	runonce=1

            	if num == 4 and runonce == 0:
                	tempSplit = response.split(":")
                	temppSplit = tempSplit[1].split(",")
                	if temppSplit[0] < 5:
                         	print ("RSSI TO LOW "+temppSplit[0])
                         	logging.error("RSSI TO LOW "+temppSplit[0])
                	else:
                		okay = okay+1
                        	print("RSSI OK "+temppSplit[0])
                        	logging.error("RSSI OK "+temppSplit[0])
                	runonce=1

            	if num == 5 and runonce == 0:
                	tempSplit = response.split(",")
                	batteryPercent = tempSplit[1]
                	voltageLevel = tempSplit[2]
                	print ("BATTERY LEVEL: "+batteryPercent)
                	print ("VOLTAGE LEVEL: "+voltageLevel)
                	logging.error("BATTERY LEVEL: "+batteryPercent)
                	logging.error("VOLTAGE LEVEL: "+voltageLevel)
                	if batteryPercent < 10:
                    		print ("CRITICAL BATTERY LEVEL REACHED: "+batteryPercent)
                    		logging.error("CRITICAL BATTERY LEVEL REACHED " +batteryPercent)
                    		fail=9000
                	else:
                    		okay = okay+1
                	if voltageLevel < 3300 and voltageLevel > 4200:
                    		print ("CRITICAL VOLTAGE LEVEL REACHED: "+voltageLevel)
                    		logging.error("CRITICAL VOLTAGE LEVEL REACHED "+voltageLevel)
                    		fail=9000
                	else:
                    		okay = okay+1
                    
                	runonce=1
            	if num == 6 and runonce == 0:
                	print ("REQUEST GPS FIX ")
                	print("THIS MAY TAKE SOME TIME...")
                	runonce=1
			time.sleep(2)
            	if num == 6:
                	tempSplit = response.split(",")
                	fix = tempSplit[1]
                	if fix=="1":
                    		okay = okay+1
                    		latitude = tempSplit[3]
                    		longitude = tempSplit[4]
                    		print ("LATITUDE: "+latitude)
                    		print ("LONGITUDE: "+longitude)
                    		logging.error("LATITUDE: "+latitude)
                    		logging.error("LONGITUDE: "+longitude)
				#os.system("sudo pon fona")
				#time.sleep(3)
				#coords = {"longitude": longitude,"latitude": latitude}
				#firebase.post('/coordinates',coords)
				#os.system("sodo poff fona")
				
                
            	print("\n"+response+"\n")
        if "OK" in response:
        	if num == 6 and fix == "0":
                	fail = fail+1
			time.sleep(0.5)
                	ser.write(cmd)
            	else: 
                	print ("OK")
                	logging.error(" OK\n\r")
                	num = num+1
                	fail=0
                	break
        if fail >300:
        	print("TIMEOUT")
            	logging.error("TIMEOUT\n\r")
            	break
            
        if "ERROR" in response:
            	print ("ERROR")
            	logging.error(" ERROR\n\r")
            	num = num+1
            	break

        if last_cmd == num:
            	break
     
print(okay)
if okay >=5:
	print ("STARTUP SUCCESS!")
    	logging.error(" LAST STARTUP SUCCESS!\n\r")
	import bt_test
else:
    	print("STARTUP FAILED...")
    	logging.error(" LAST STARTUP FAILED!\n\r")
	logging.error("PLEASE RESTART  DEVICE AND CHECK ERRORS\n\r")


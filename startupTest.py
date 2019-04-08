import serial
import time
import os
ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)
fail = 0
testsPassed = 0
f=open("startuplog.txt","w+")
f.write("Startup log\n\r")
print "REQUEST UART CONNECTION TO FONA808...\n\r"
f.write("TESTING AT ")
ser.write("AT\r")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "UART CONNECTION PASSED.\n\r"
		testsPassed = testsPassed + 1
		break

	else:
		print "UART CONNECTION FAILED\n\r"
		break
		
ser.write("AT+CGNSPWR=1\r")
ser.write("AT+CGNSPWR?\r")

print "CHECKING FONA808 POWERSTATUS...\n\r"
f.write("TESTING FONA808 POWER")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	print response
	if "1" in response:
		print("POWER OK...\n\r")
		testsPassed = testsPassed + 1
		break
		
	else:
		print "POWER REQUEST ERROR\n\r"
		break
		

ser.write("AT+CBC\r")

print "CHECKING FONA808 BATTERY LEVELS...\n\r"
f.write("TESTING FONA808 BATTERY")

while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "+CBC:" in response:
		tempSplit = response.split(",")
		batteryPercent = tempSplit[1]
		voltageLevel = tempSplit[2]
		print ("BATTERY LEVEL: "+batteryPercent)
		print ("VOLTAGE LEVEL: "+voltageLevel)
		break
	else:
		print "BATTERY REQUEST ERROR\n\r"
		break

ser.write("AT+CGNSINF\r")

print "CHECKING GPS FIX...\n\r"
f.write("TESTING GPS FIX")

while True:
	response = ser.readline()
	if "+CGNSINF: 1,1" in response:
		print "SATALLITE FIXED\n\r"
		testsPassed = testsPassed + 1
		f.write("SATALLITE CONNECTION SUCCESS")
		break

	else:
		fail = fail +1
		time.sleep(2)
		ser.write("AT+CGNSINF\r")

	if fail>100:
		print "CONNECTION TO SATALLITE FAILED\n\r"
		f.write("SATALLITE CONNECTION FAILED")
		break


ser.write("AT+CGNSINF\r")

print "REQUESTING GPS COORDINATES...\n\r"
f.write("FETCHING GPS COORDINATES")

while True:
	response = ser.readline()
	if "+CGNSINF: 1,1" in response:
		testsPassed = testsPassed + 1
		tempSplit = response.split(",")
		lat = tempSplit[3]
		long = tempSplit[4]
		print("LATITUDE: "+lat)
		print("LONGITUDE: "+long)
		f.write("\nLatitude: " +lat)
		f.write("\nLongitude: " +long)
		f.write("FETCHING SUCCESS")
		break
	else:
		fail = fail +1
		time.sleep(2)
		ser.write("AT+CGNSINF\r")

	if fail>100:
		print "GPS COORDINATES COULD NOT BE READ...\n\r"
		f.write("FETCHING FAILED")
		break


#GPS INIT TEST OK...START SIM TEST...
ser.write("AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r")

print "INIT GPRS/HTTP...\n\r"
f.write("TESTING GPRS/HTTP")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "AT+SAPBR 3,1 OK\n\r"
		testsPassed = testsPassed + 1
		break
	else:
		print "AT+SAPBR 3,1 ERROR\n\r"
		break
		
ser.write("AT+SAPBR=1,1\r")

while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "AT+SAPBR 1,1 OK\n\r"
		testsPassed = testsPassed + 1
		break
	else:
		print "AT+SAPBR 1,1 ERROR\n\r"
		break
ser.write("AT+SAPBR=2,1\r")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "AT+SAPBR 2,1 OK\n\r"
		testsPassed = testsPassed + 1
		break
	else:
		print "AT+SAPBR 2,1 ERROR\n\r"
		break
		
ser.write("AT+HTTPINIT\r")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "HTTPINIT OK\n\r"
		testsPassed = testsPassed + 1
		break
	else:
		print "AT+HTTPINIT ERROR\n\r"
		break
		
ser.write("AT+HTTPPARA=\"CID\",1\r")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "HTTPPARA OK\n\r"
		testsPassed = testsPassed + 1
		break
	else:
		print "AT+HTTPPARA ERROR\n\r"
		break

print "SET URL TO FIREBASE...\n\r"
ser.write("AT+HTTPPARA=\"URL\",\"HTTP://XXXXXXXXXXXXXXXX \r")
while True:
	response = ser.readline()
	f.write(respone+"\n\r")
	if "OK" in response:
		print "URL OK\n\r"
		testsPassed = testsPassed + 1
		break
	else:
		print "URL ERROR\n\r"
		break
		
if testsPassed >=10
	print "STARTUP SUCCESS!"
else
	print "RABBIT STARTUP FAILED CHECK LOG..."
f.close()	
	
	
	
	
	



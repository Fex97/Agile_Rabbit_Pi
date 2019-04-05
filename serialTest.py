import serial
import time

ser=serial.Serial('/dev/serial0', 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
ser.write("AT+CGNSPWR=1\r")
ser.write("AT+CGNSPWR?\r")

print "Checking FONA808 powerstatus...."

while True:
	response = ser.readline()
	print response
	if "1" in response:
		print("Power is on")
		break

ser.write("AT+CBC\r")

print "Checking for battery levels..."

while True:
	response = ser.readline()
	if "+CBC: 0" in response:
		tempSplit = response.split(",")
		batteryPercent = tempSplit[1]
		voltageLevel = tempSplit[2]
		print ("Battery percent = "+batteryPercent)
		print ("Voltage level = "+voltageLevel)
		break

ser.write("AT+CGNSINF\r")

print "Checking GPS coordinates...."

while True:
	response = ser.readline()
	if "+CGNSINF: 1,1" in response:
		tempSplit = response.split(",")
		lat = tempSplit[3]
		long = tempSplit[4]
		print("Latitude = "+lat)
		print("Longitude = "+long)
		f=open("cooords.txt","w+")
		f.write("\nLatitude: " +lat)
		f.write("\nLongitude: " +long)
		f.close()
		break
	if "+CGNSINF: 1,0" in response:
		time.sleep(4)
		ser.write("AT+CGNSINF\r")
	else:
		time.sleep(4)
		ser.write("AT+CGNSINF\r")

import testpy

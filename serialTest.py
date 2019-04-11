import serial
import time
from firebase import firebase
firebase=firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com', None)

ser=serial.Serial('/dev/serial0', 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
ser.write("AT+CGNSPWR=1\r")
ser.write("AT+CGNSPWR?\r")

print "CHECKING FONA808 POWERSTATUS...\n\r"

while True:
	response = ser.readline()
	print response
	if "1" in response:
		print("POWER OK...\n\r")
		break

ser.write("AT+CBC\r")

print "CHECKING FONA808 BATTERY LEVELS...\n\r"

while True:
	response = ser.readline()
	if "+CBC: 0" in response:
		tempSplit = response.split(",")
		batteryPercent = tempSplit[1]
		voltageLevel = tempSplit[2]
		print ("BATTERY LEVEL: "+batteryPercent)
		print ("VOLTAGE LEVEL: "+voltageLevel)
		break

ser.write("AT+CGNSINF\r")

print "REQUESTING GPS COORDINATES...\n\r"

while True:
	response = ser.readline()
	if "+CGNSINF: 1,1" in response:
		tempSplit = response.split(",")
		lat = tempSplit[3]
		long = tempSplit[4]
		print("LATITUDE: \n\r"+lat)
		print("LONGITUDE: \n\r"+long)
		cords = {"long": long, "lat": lat}
		firebase.post('/coords', cords)
		break
	if "+CGNSINF: 1,0" in response:
		time.sleep(4)
		ser.write("AT+CGNSINF\r")
	else:
		time.sleep(4)
		ser.write("AT+CGNSINF\r")

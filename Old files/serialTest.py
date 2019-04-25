import serial
import time
from firebase import firebase
import os
firebase=firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com', None)

ser=serial.Serial('/dev/serial0', 115200, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
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
		os.system("sudo pon fona")
		time.sleep(3)
		cords = {"long": long, "lat": lat}
		firebase.post('/coords', cords)
		os.system("sudo poff fona")
		break
	if "+CGNSINF: 1,0" in response:
		time.sleep(4)
		ser.write("AT+CGNSINF\r")
	else:
		time.sleep(4)
		ser.write("AT+CGNSINF\r")

import bt_test

import serial
import time
import os
ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)
fail = 0
testsPassed = 0
print "CHECKING UART CONNECTION TO FONA808...\n\r"
ser.write("AT\r")
while True:
	response = ser.readline()
	if "OK" in response:
		print "UART CONNECTION PASSED.\n\r"
		testsPassed = testsPassed + 1
		break

	else:
		fail = fail + 1
		time.sleep(2)
		ser.write("AT\r")

	if  fail>5:
		fail = 0
		print "UART CONNECTION FAILED\n\r"
		break

print "CHECKING GPS FIX...\n\r"
ser.write("AT+CGNSINF\r")

while True:
	response = ser.readline()
	if "+CGNSINF: 1,1" in response:
		print "SATALLITE FIXED\n\r"
		testsPassed = testsPassed + 1
		break

	else:
		fail = fail +1
		time.sleep(2)
		ser.write("AT+CGNSINF\r")

	if fail>100:
		print "CONNECTION TO SATALLITE FAILED\n\r"
		break

if testsPassed >=2:
	import serialTest



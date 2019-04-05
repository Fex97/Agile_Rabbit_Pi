import serial
import time

ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)
fail = 0
ser.write("AT\r")
while True:
	response = ser.readline()
	if "OK" in response:
		break

	else:
		fail = fail +1
		time.sleep(2)
		ser.write("AT\r")

	if  fail>5:
		fail = 0
		print "UART CONNECTION FAILED\n"
		break

ser.write("AT+CGNSINF\r")

while True:
	response = ser.readline()
	if "+CGNSINF: 1,1" in response:
		break

	else:
		fail = fail +1
		time.sleep(2)
		ser.write("AT+CGNSINF\r")

	if fail>10:
		print "CONNECTION TO SATALITE FAILED\n"
		break

ser.write("AT+CBC")


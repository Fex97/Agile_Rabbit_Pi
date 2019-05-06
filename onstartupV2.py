import serial
import logging
import time
import os
import databaseFb
import RPi.GPIO as GPIO


redled = 11
greenled = 13

def init_leds():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(redled,GPIO.OUT,initial =0)
	GPIO.setup(greenled,GPIO.OUT,initial=0)

def check_uartConnection(ser):
	print("1")
	ser.write("AT\r")
	fails = 0
	while True:
		response=ser.readline()
		if "OK" in response:
			return True
		if fails>5:
			return False
		fails = fails + 1
		time.sleep(1)

def set_CGNSPower(ser):
	ser.write("AT+CGNSPWR=1\r")
	print("2")
	fails = 0
	while True:
		response = ser.readline()
		if "OK" in response:
			return True
		if fails>5:
			return False
		fails = fails + 1
		time.sleep(1)

def check_CGNSPower(ser):
	print("3")
	ser.write("AT+CGNSPWR=1\r")
	fails = 0
	while True:
		response = ser.readline()
		if "1" in response:
			logging.error("GNSS IS ON")
			return True
		if fails>5:
			logging.error("GNSS IS OFF")
			return False
		fails = fails + 1
		time.sleep(1)

def check_RSSI(ser):
	print("4")
	ser.write("AT+CSQ\r")
	fails = 0
	while True:
		response = ser.readline()
		if "+CSQ:" in response:
			tempSplit = response.split(":")
			tempSplit2 = tempSplit[1].split(",")
			if int(tempSplit2[0]) > 5:
				logging.error("RSSI OK "+tempSplit2[0])
				return True
			if int(tempSplit2[0]) <=5:
				logging.error("RSSI to low "+tempSplit2[0])
				return False
		if fails > 5:
			logging.error("CSQ FAIL")
			return False
		fails = fails + 1
		time.sleep(1)

def check_batteryLevel(ser):
	print("5")
	ser.write("AT+CBC\r")
	fails = 0
	while True:
		response = ser.readline()
		if "+CBC:" in response:
			tempSplit = response.split(",")
			batteryPercent = tempSplit[1]
			voltageLevel = tempSplit[2]
			logging.error("BATTERY LEVEL: "+batteryPercent)
			logging.error("VOLTAGE LEVEL: "+voltageLevel)
			if int(batteryPercent) < 10:
				logging.error("CRITICAL BATTERY LEVEL REACHED " +batteryPercent)
				return False
			if int(voltageLevel) < 3300 or int(voltageLevel) > 4300:
				logging.error("CRITICAL VOLTAGE LEVEL REACHED "+voltageLevel)
				return False
			else:
				return True
		if fails > 5:
			logging.error("Battery Fail")
			return False
		fails = fails + 1
		time.sleep(1)

def check_gpsFix(ser):
	ser.write("AT+CGNSINF\r")
	print("6")
	fails = 0
	while True:
		response = ser.readline()
		if "+CGNSINF:" in response:
			tempSplit = response.split(",")
			fix = tempSplit[1]
			if fix == "1":
				logging.error("GPS fix found")
				return True

		if fails >100:
			logging.error("GPS fix not found")
			return False
		fails = fails + 1
		time.sleep(1)

def get_coordinates(ser):
	print("7")
	ser.write("AT+CGNSINF\r")
        fails = 0
        while True:
		response = ser.readline()
                if "+CGNSINF:" in response:
                        tempSplit = response.split(",")
                        latitude = tempSplit[3]
                        longitude = tempSplit[4]
                        return latitude,longitude
                if fails > 5:
                        return 0

                fails = fails + 1
                time.sleep(1)


def mainstart():
	os.system("sudo poff fona")
	ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)
	logging.basicConfig(filename='startup.log', filemode='w', format='%(message)s')

	init_leds()
	#deleted check_fix() function call.
	if check_uartConnection(ser) and set_CGNSPower(ser) and check_CGNSPower(ser)and check_RSSI(ser) and check_batteryLevel(ser):
		print("OK")
                logging.error("All tests passed")
                #latitude,longitude = get_coordinates(ser)
		os.system("sudo pon fona")
		time.sleep(3)
		#databaseFb.db_upload('/coordinates','Latitude',latitude)
                #databaseFb.db_upload('/coordinates','Longitude',longitude)
		GPIO.output(greenled,1)
		GPIO.output(redled,0)
                #import main
		return True
	else:
		print("FAILED")
		logging.error("Start up tests failed.")
		GPIO.output(greenled,0)
		GPIO.output(redled,1)
		return False

if __name__ == "__main__":
	#mainstart()
	if(mainstart()):
		os.system("cd/programs/git/Agile_Rabbit_Pi")
		os.system("python main.py")




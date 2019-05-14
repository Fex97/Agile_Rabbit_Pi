import serial
import logging
import time
import os
import databaseFb
import RPi.GPIO as GPIO
from subprocess import call

redled = 11
greenled = 13

#---------------------------------------------------------------------------------
# init_leds()
# Gpio initialization for the leds.
#---------------------------------------------------------------------------------
def init_leds():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(redled,GPIO.OUT,initial =0)
	GPIO.setup(greenled,GPIO.OUT,initial=0)

#---------------------------------------------------------------------------------
# check_uartConnection(ser) where ser is a serial connection
# Sends "AT" to fona808 via uart and checks if "OK" is returned back to se that the
# uart connection is ok.
#---------------------------------------------------------------------------------
def check_uartConnection(ser):
	print("1")
	fails = 0
	while True:
		ser.write("AT\r")
		response=ser.readline()
		if "OK" in response:
			logging.info("UART CONNECTION OK")
			return True
		if fails>5:
			logging.error("UART CONNECTION FAIL")
			return False
		fails = fails + 1
		time.sleep(1)

#---------------------------------------------------------------------------------
# set_CGNSPower(ser) where ser is a serial connection
# Sends "AT+CGNSPWR=1" to fona808 via uart to set CGNSPower to 1.
#---------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------
# check_CGNSPower(ser) where ser is a serial connection
# Sends "AT+CGNSPWR?" to fona808 via uart to check if CGNS power is on(1).
#---------------------------------------------------------------------------------
def check_CGNSPower(ser):
	print("3")
	ser.write("AT+CGNSPWR=1\r")
	fails = 0
	while True:
		response = ser.readline()
		if "1" in response:
			logging.info("GNSS IS ON")
			return True
		if fails>5:
			logging.error("GNSS IS OFF")
			return False
		fails = fails + 1
		time.sleep(1)

#---------------------------------------------------------------------------------
# check_RSSI(ser) where ser is a serial connection
# Sends "AT+CSQ" to fona808 via uart to check RSSI level. If its too low return
# False. If RSSI is OK return True.
#---------------------------------------------------------------------------------
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
				logging.info("RSSI OK "+tempSplit2[0])
				return True
			if int(tempSplit2[0]) <=5:
				logging.error("RSSI to low "+tempSplit2[0])
				return False
		if fails > 5:
			logging.error("CSQ FAIL")
			return False
		fails = fails + 1
		time.sleep(1)

# ---------------------------------------------------------------------------------
# check_batteryLevel(ser) where ser is the serial connection
# Sends "AT+CBC" to fona 808 via uart and checks if "+CBC" is returned.
# If it's the correct response, checks if the returned batterylevel is within safe
# margins. Returns true if OK, else False.
# ---------------------------------------------------------------------------------
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
			logging.info("BATTERY LEVEL: "+batteryPercent)
			logging.info("VOLTAGE LEVEL: "+voltageLevel)
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

# ---------------------------------------------------------------------------------
# check_gpsFix(ser) where ser is the serial connection
# Sends "AT+CGNSINF" to fona 808 via uart and checks if "+CGNSINF" is returned.
# If it's the correct response, checks if the "fix" variable is 1. Else try again
# maxFixFails number of times. 
# ---------------------------------------------------------------------------------
def check_gpsFix(ser):
	maxFixFails = 150
	print("6")
	fails = 0
	while True:
		ser.write("AT+CGNSINF\r")
		time.sleep(1)
		GPIO.output(redled,1)
		response = ser.readline()
		print(response)
		if "+CGNSINF:" in response:
			tempSplit = response.split(",")
			fix = tempSplit[1]
			if fix == "1":
				logging.info("GPS fix found")
				return True
		if fails >maxFixFails:
			logging.info("GPS fix not found")
			return False
		print("GPS FIX FAIL NR:" + str(fails) + "/" + str(maxFixFails))
		fails = fails + 1
		GPIO.output(redled,0)
		time.sleep(1)

# ---------------------------------------------------------------------------------
# get_coordinates(ser) where ser is the serial connection
# Sends "AT+CGNSINF" to fona 808 via uart and checks if "+CGNSINF" is returned.
# If it's the correct response, splits the string and puts lat and long into
# variables, else try again
# ---------------------------------------------------------------------------------
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
	os.system("sudo poff fona") #Start GSM connection
	ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)
	logging.basicConfig(filename='startup.log', filemode='w', format='%(message)s')
	init_leds()
	if check_uartConnection(ser) and set_CGNSPower(ser) and check_CGNSPower(ser)and check_RSSI(ser) and check_batteryLevel(ser) and check_gpsFix(ser):
		print("OK")
                logging.error("All tests passed")
                latitude,longitude = get_coordinates(ser)
		print(longitude,latitude)
		os.system("sudo pon fona")
		time.sleep(5)
		databaseFb.db_upload('/coordinates','Latitude',latitude)
                databaseFb.db_upload('/coordinates','Longitude',longitude)
		GPIO.output(greenled,1)
		GPIO.output(redled,0)
                import BTmain
	else:
		print("FAILED")
		logging.error("Start up tests failed.")
		GPIO.output(greenled,0)
		GPIO.output(redled,1)

if __name__ == "__main__":
	mainstart()





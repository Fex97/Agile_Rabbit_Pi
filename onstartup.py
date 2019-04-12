simport serial
import logging
import time
import os
ser = serial.Serial('/dev/serial0',115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,timeout=1)

logging.basicConfig(filename='startup.log', filemode='w', format='%(message)s')

print ("STARTUP RABBIT_PI GSM module...\n\r")
logging.error("Latest Startup log")
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
    6: "AT+CGNINF\r",
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
        #response = '' 
        if "OK" in response:
            if num == 2 and runonce == 0:
                print ("PWR")
                logging.error("GMS POWER: ")
                runonce=1

            if num == 3 and runonce == 0:
                print ("COPS")
                logging.error("COPS: ")
                runonce=1

            if num == 4 and runonce == 0:
                print ("RSSI")
                logging.error("RSSI: ")
                runonce=1

            if num == 5 and runonce == 0:
                tempSplit = response.split(",")
                batteryPercent = tempSplit[1]
                voltageLevel = tempSplit[2]
                print ("BATTERY LEVEL: "+batteryPercent+"\n\r")
                print ("VOLTAGE LEVEL: "+voltageLevel+"\n\r")
                logging.error("BATTERY LEVEL: "+batteryPercent)
                logging.error("VOLTAGE LEVEL: "+voltageLevel)
                runonce=1
            if num == 6 and runonce == 0:
                print ("REQUEST GPS FIX ")
                print("THIS MAY TAKE SOME TIME...")
                runonce=1
            
            okay = okay+1
            print ("cmd: ",cmd," SUCCESS ")
            logging.error(" SUCCESS\n\r")
            num = num+1
            fail=0
            break
        else:
            fail = fail +1
            ser.write(str(cmd))
            
            if num == 6:
                time.sleep(0.5)
                if fail>300:
                    print ("cmd: ",cmd," ERROR ")
                    logging.error(" ERROR\n\r")
                    num = num+1
                    fail=0
                    break
            else:
                if fail>50:
                    print ("cmd: ",cmd," ERROR ")
                    logging.error(" ERROR\n\r")
                    num = num+1
                    fail=0
                    break
        if last_cmd == num:
            break
     
if okay >=last_cmd:
    print ("STARTUP SUCCESS!")
    logging.error(" LAST STARTUP SUCCESS!\n\r")
else:
    print("STARTUP FAILED...")
    logging.error(" LAST STARTUP FAILED!\n\r")



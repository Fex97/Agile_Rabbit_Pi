import serial
import logging
import time
import os
ser = serial.Serial('/dev/serial0',
                                        115200,bytesize=serial.EIGHTBITS,
                                        parity=serial.PARITY_NONE,
                                        stopbits=serial.STOPBITS_ONE,
                                        timeout=1)
                                            
logging.basicConfig(filename='startup.log', filemode='w', format='%(levelname)s - %(message)s')

print ("INIT RABBITPI\n\r")
logging.INFO("Latest Startup log")
cmd=1
last_cmd=12
fail=0
okay=0
def switch_cmd(num):
    switcher = {
        1: "AT\r",
        2: "AT+CGNSPWR=1\r",
        3: "AT+CGNSPWR?\r",
        4: "AT+COPS?\r",
        5: "AT+CSQ\r",
        6: "AT+CBC\r",
        #INSERT GPS HERE TO GET DATE AND COORDS BEFORE SIM
        7: "AT+SAPBR=3,1,\"CONTYPE\",\"GPRS\"\r",
        8: "AT+SAPBR=1,1\r",
        9: "AT+SAPBR=2,1\r",
        10: "AT+HTTPINIT\r",
        11: "AT+HTTPPARA=\"CID\",1\r",
        12: "AT+HTTPPARA=\"URL\",\"HTTP://XXXXXXXXXXXXXXXX\r"
    }
while True:
        cmd = switcher(num)
        ser.write(cmd)
        logging.INFO(cmd+" ")
        runonce=false
        while True:
                response = ser.readline()
                #Specialcases before OK
                #NOTDONE
                if num == 3 and runonce == false:
                        print ("PWR\n\r")
                        runonce=true
                #NOTDONE
                if num == 4 and runonce == false:
                        print ("COPS\n\r")
                        runonce=true
                #NOTDONE
                if num == 5 and runonce == false:
                        print ("RSSI\n\r")
                        runonce=true
                #batterycheck
                if num == 6 and runonce == false:
                        tempSplit = response.split(",")
                        batteryPercent = tempSplit[1]
                        voltageLevel = tempSplit[2]
                        print ("BATTERY LEVEL: "+batteryPercent+"\n\r")
                        print ("VOLTAGE LEVEL: "+voltageLevel+"\n\r")
                        logging.INFO("BATTERY LEVEL: "+batteryPercent)
                        logging.INFO("VOLTAGE LEVEL: "+voltageLevel)
                        runonce=true
                if "OK" in response:
                        okay = okay+1
                        print ("cmd: ",cmd," SUCCESS \n\r")
                        logging.INFO(" SUCCESS\n\r")
                        num = num+1
                        fail=0
                        break
                else:
                        fail = fail +1
                        time.sleep(2)
                        ser.write(cmd)

                if fail>50:
                        print ("cmd: ",cmd," ERROR \n\r")
                        logging.ERROR(" ERROR\n\r")
                        num = num+1
                        fail=0
                        break
        if last_cmd == num:
                break
if okay >=last_cmd:
        print ("STARTUP SUCCESS!\n\r")
else:
        print ("STARTUP FAILED."+okay+"/"+last_cmd+"\n\r")
            


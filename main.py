import bluetooth
import time
from datetime import date
from datetime import datetime
import databaseFb
from threading import Thread
import collections
import re

def bluetooth_scan():
        maxunits = 5
        timeoutm = 1
	devicelist = []
	num = 0
	lastadded = 0
	atime = 0
	devfound = False
	while True:
		nrby = bluetooth.discover_devices(duration=2)
		for item in nrby:
			if not item in devicelist:
				print(item)
				devicelist.append(item)
				num = num+1
				devfound = True
				lastadded = datetime.now()

		atime = datetime.now()
		if devfound == False:
			lastadded= atime

		if num>=maxunits or abs(atime.minute-lastadded.minute)>=timeoutm:
			for x in devicelist:
				buffer.append(x)
			devicelist = []

def bluetooth_compareToUsers():
	while True:
		if len(buffer) is not 0:
			value = buffer.popleft()
			with open('users.txt', 'r') as userList:
				for line in userList:
					if value in line:
						print("User found, uploading flag")
						string = "/Users/{}".format(value)
						date = datetime.now()
						dateTime = re.findall(r"\d{4}.\d{2}.\d{2}.\d+.\d+","{}".format(date))
						tmpTime= dateTime[0]
						tmpTime = tmpTime.replace('T',',')
						databaseFb.db_upload(string,'/timestamp', "{}".format(tmpTime))
			userList.close()
			
if __name__=="__main__":

	buffer = collections.deque(maxlen=50)

	t1 = Thread(target=bluetooth_scan)
	t2 = Thread(target=bluetooth_compareToUsers)

	t1.start()
	t2.start()

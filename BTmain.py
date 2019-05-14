import bluetooth
import time
import databaseFb
import collections
import re
from datetime import date
from datetime import datetime
from threading import Thread

def bluetooth_scan():
        maxunits = 25
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
				print(num)
				devfound = True
				lastadded = datetime.now()

		atime = datetime.now()
		if devfound == False:
			lastadded= atime

		if num>=maxunits or abs(atime.minute-lastadded.minute)>=timeoutm:
			for x in devicelist:
				buffer.append(x)
			devicelist = []
			num=0

def bluetooth_compareToUsers():
	while True:
		if len(buffer) is not 0:
			value = buffer.popleft()
			if databaseFb.db_compare('/Users',value):
				print("Found user")
				string = "/Users/{}".format(value)
				date = datetime.now()
				dateTime = re.findall(r"\d{4}.\d{2}.\d{2}.\d+.\d+","{}".format(date))
				tmpTime= dateTime[0]
				tmpTime = tmpTime.replace('T',',')
				databaseFb.db_upload(string,'/timestamp', "{}".format(tmpTime))

if __name__=="BTmain":
	buffer = collections.deque(maxlen=50)

	t1 = Thread(target=bluetooth_scan)
	t2 = Thread(target=bluetooth_compareToUsers)

	t1.start()
	t2.start()

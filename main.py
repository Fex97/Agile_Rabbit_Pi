import bluetooth
import time
from datetime import date
from datetime import datetime
import databaseFb
from threading import Thread
import collections
import re

def bluetooth_appendlist(item,devicelist):
	global lastadded
	if not item in devicelist:
		print(item)
		devicelist.append(item)
		lastadded = datetime.now()

	return devicelist


def bluetooth_scan():
        maxunits = 25
        timeoutm = 1
	devicelist = []
	num = 0
	atime = 0
	while True:
		nrby = bluetooth.discover_devices(duration=2)
		for item in nrby:
			bluetooth_appendlist(item,devicelist)
		atime = datetime.now()
		if num>=maxunits or abs(atime.minute-lastadded.minute)>=timeoutm:
			for x in devicelist:
				buffer.append(x)
			devicelist = []

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

if __name__=="__main__":
	lastadded = 0
	buffer = collections.deque(maxlen=500)

	t1 = Thread(target=bluetooth_scan)
	t2 = Thread(target=bluetooth_compareToUsers)

	t1.start()
	t2.start()


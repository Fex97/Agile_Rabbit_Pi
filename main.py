import bluetooth
import time
from datetime import date
from datetime import datetime
from databaseFb import db_compare
from databaseFb import db_upload
from threading import Thread
import collections

def bluetooth_scan():
	devicelist = []
	num = 0
	lastadded = 0
	atime = 0
	devfound = False
	while True:
		#print("HEJ\n")
		nrby = bluetooth.discover_devices(duration=1)
		for item in nrby:
			if not item in devicelist:
				devicelist.append(item)
				num = num+1
				devfound = True
				lastadded = datetime.now()

		atime = datetime.now()
		if devfound == False:
			lastadded= atime


		if num>=2 or abs(atime.minute-lastadded.minute)>=1:
			for x in devicelist:
				buffer.append(x)

			devicelist = []



def bluetooth_compareToUsers():
	while True:
		#print("da\n")
		if len(buffer) is not 0:
			value = buffer.popleft()
			if not db_compare('/devices',value):
				db_upload('/devices',value,'tid')

		time.sleep(1)




if __name__=="__main__":
	buffer = collections.deque(maxlen=50)

	t1 = Thread(target=bluetooth_scan)
	t2 = Thread(target=bluetooth_compareToUsers)

	t1.start()
	t2.start()

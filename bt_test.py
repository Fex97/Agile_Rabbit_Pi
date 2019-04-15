import bluetooth
import time
from datetime import date

from datetime import datetime
print("\n\rSTARTED BLUETOOTH SCANNING\n\r")
devicelist = []
num=0
lastadded =0
atime=0
devfound =False
while True:
	nrby = bluetooth.discover_devices(duration=2,lookup_names=True)
	for item in nrby:
		print("\n\r")
		print(item)
		if item in devicelist:
			print("DEVICE ALREADY IN LIST\n\r")
		else:
			devicelist.append(item)
			print("NEW DEVICE ADDED TO LIST\n\r")
			num=num+1
			devfound =True
			lastadded = datetime.now()
	#for x in devicelist:
		#print(x)
	atime = datetime.now()
	if devfound ==False:
		lastadded= atime

	if num >= 5:
		print("COMPARE TO FIREBASE\n\r")
		for x in devicelist:
			print(x)
		time.sleep(3)
		devicelist = []
		devfound=False
	#TIMEOUT IF
	if abs(atime.minute - lastadded.minute) >=1:
		print("TIMEOUT\n\r")
		print("COMPARE TO FIREBASE\n\r")
		for x in devicelist:
			print(x)
		time.sleep(3)
		devicelist =[]
		devfound=False
	

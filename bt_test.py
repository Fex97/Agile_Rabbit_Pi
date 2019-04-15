import bluetooth
import time

print("TEST STARTED ON BT")
devicelist = []
while True:
	print("CHECKING")
	nrby = bluetooth.discover_devices(duration=2,lookup_names=True)
	for item in nrby:
		if item in devicelist:
			print("DEVICE ALREADY IN LIST")
		else:
			devicelist.append(item)
			print("NEW DEVICE ADDED TO LIST")
	for x in devicelist:
		print(x)

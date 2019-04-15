import bluetooth
import time

print("TEST STARTED ON BT")
devicelist = []
while True:
	print("CHECKING")
	nrby = bluetooth.discover_devices(duration=2,lookup_names=True)
	for addr in nrby:
		if nrby in devicelist:
			print("DEVICE ALREADY IN LIST")
		else:
			devicelist.append(nrby)
			print("NEW DEVICE ADDED TO LIST")
	for x in devicelist:
		print(x)

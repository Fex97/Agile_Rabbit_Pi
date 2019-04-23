import bluetooth
import time
from datetime import date
from firebase import firebase
from datetime import datetime
import os

#firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)

def mainloop(firebase):
	print("\n\rSTARTED BLUETOOTH SCANNING\n\r")
	devicelist = []
	num=0
	lastadded =0
	atime=0
	devfound =False
	while True:
	#kolla global env var to see if crontab is active
	
	
		nrby = bluetooth.discover_devices(duration=2)
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
			os.system("sudo pon fona")
			time.sleep(3)
			enheter = firebase.get('/devices',None)
			for y in devicelist:
				if not y in enheter:
					print("not exist\n")
					firebase.put('/devices',y,datetime.now())
				else:
					print("already exists\n")
			os.system("sudo poff fona")
			devicelist = []
			devfound=False
			num = 0
		#TIMEOUT IF
		if abs(atime.minute - lastadded.minute) >=1:
			print("TIMEOUT\n\r")
			print("COMPARE TO FIREBASE\n\r")
			os.system("sudo pon fona")
			time.sleep(3)
			enheter = firebase.get('/devices',None)
			for y in devicelist:
				if not y in enheter:
					print("not exist\n")
					firebase.put('/devices',y,datetime.now())
				else:
					print("already exists\n")
			os.system("sudo poff fona")
			devicelist =[]
			devfound=False
			lastadded=0
			num = 0
def main():
	firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)
	mainloop(firebase)
if __name__ == "__main__":
	main()
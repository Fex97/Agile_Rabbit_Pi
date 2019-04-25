from firebase import firebase
import time
import os

firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)

def db_upload(dir,value1,value2):
	os.system("sudo pon fona")
	time.sleep(3)
	firebase.put(dir,value1,value2)
	os.system("sudo poff fona")
	time.sleep(1)

def db_update(dir,child,value):
	os.system("sudo pon fona")
	time.sleep(3)
	dir = ("{}/{}".format(dir,child))
	firebase.update({ dir : value})
	os.system("sudo poff fona")
	time.sleep(1)

def db_download(dir):
	os.system("sudo pon fona")
	time.sleep(3)
	result = firebase.get(dir, None)
	os.system("sudo poff fona")
	time.sleep(1)
	return result

def db_compare(dir,value):
	os.system("sudo pon fona")
	time.sleep(3)
	result=firebase.get(dir,None)
	os.system("sudo poff fona")
	time.sleep(1)
	if value in result:
		return True
	else:
		return False

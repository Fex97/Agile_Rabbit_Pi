from firebase import firebase
import time
import os

firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)

def db_upload(dir,value1,value2):
	print("database upload")
	firebase.put(dir,value1,value2)

def db_update(dir,child,value):
	dir = ("{}/{}".format(dir,child))
	firebase.update({ dir : value})

def db_download(dir):
	result = firebase.get(dir, None)
	return result

def db_compare(dir,value):
	string = ("{}/{}".format(dir,value))
	result=firebase.get(string,None)
	if result == None:
		return False
	else:
		return True

from firebase import firebase
import time

firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)

	
def db_upload(dir,value):
	firebase.put(dir,value)
	time.sleep(2)
	
	
		
def db_download(dir):
	result = firebase.get(dir, None)
	time.sleep(2)
	return result

		
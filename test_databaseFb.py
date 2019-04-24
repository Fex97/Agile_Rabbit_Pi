import unittest
import databaseFb
from firebase import firebase
import os
import time

class TestDatabase(unittest.TestCase):
	def test_upload(self):
		databaseFb.db_upload('/test', "test", '')
		os.system("sudo pon fona")
		time.sleep(3)
		result = firebase.get('/test', None)
		self.assertTrue("test" in result)
		firebase.delete('/test','')
		os.system("sudo poff fona")
		time.sleep(1)

	def test_download(self):
		os.system("sudo pon fona")
		time.sleep(3)
		firebase.put('/test','test2','')
		os.system("sudo poff fona")
		time.sleep(1)
		result2 = databaseFb.db_download('/test')
		self.assertTrue("test2" in result2)
		os.system("sudo pon fona")
		time.sleep(3)
		firebase.delete('/test','')
		os.system("sudo poff fona")
		time.sleep(1)
if __name__ == '__main__':
	firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)
	unittest.main()

import unittest
import databaseFb
from firebase import firebase

firebase = firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com',None)

class TestDatabase(unittest.TestCase):
	
	def test_upload(self):
		db_upload('/test', test)
		result = firebase.get('/test', None)
		assertEqual(test, result)
		
	def test_download(self):
		firebase.put('/test',test2)
		result2 = db_download('/test',None)
		assertEqual(test2,result2)
		
if __name__ == '__main__':
	unittest.main()
from firebase import firebase
import json
import urllib2,urllib,httplib
import os
from functools import partial


firebase=firebase.FirebaseApplication('https://agiltprojekt.firebaseio.com', None)

f=open("coords.txt","r")
contents = f.read()
f.close()
coords = contents.split(",")
long = coords[0]
lat = coords[1]

cords = {"long": coords[0], "lat": coords[1]}

firebase.post('/coords', cords)


print "coordinates is sendt to firebase"




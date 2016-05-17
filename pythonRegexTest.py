import serial
import re

lat = re.compile("(\d+`\d+'\d+\.\d+\" N)")
lon = re.compile("(\d+`\d+'\d+\.\d+\" E)")

ard = serial.Serial("/dev/ttyACM0")
while(True):
    data = ard.readline()
    #print data
    latDat = lat.search(data)
    lonDat = lon.search(data)

    if latDat != None:
        print latDat.group()
    if lonDat != None:
        print lonDat.group()

ard.close()

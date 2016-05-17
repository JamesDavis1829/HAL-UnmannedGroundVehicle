#!/usr/bin/env python
import rospy
import roslib
import serial
import re
from std_msgs.msg import String
from sensor_msgs.msg import Image


def cvTalker():
    pubLat = rospy.Publisher('gps_lat',String, queue_size = 10)
    pubLon = rospy.Publisher('gps_lon',String, queue_size = 10)
    rospy.init_node('gpsTalker',anonymous = True)
    rate = rospy.Rate(20)
    dev = serial.Serial('/dev/ttyACM0',9600);
    lat = re.compile("(\d+`\d+'\d+\.\d+\" N)")
    lon = re.compile("(\d+`\d+'\d+\.\d+\" E)")
    while not rospy.is_shutdown():
        data = dev.readline()
        latDat = lat.search(data)
        lonDat = lon.search(data)
        
        if lonDat != None:
            pubLat.publish(latDat.group())
        if latDat != None:
            pubLon.publish(lonDat.group())
        rate.sleep()

if __name__ == '__main__':
    try:
        cvTalker()
    except rospy.ROSInterruptException:
        pass

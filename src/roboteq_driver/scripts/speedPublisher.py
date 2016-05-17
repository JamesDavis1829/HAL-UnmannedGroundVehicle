#!/usr/bin/env python
import rospy
import serial
import roslib
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from threading import Lock
import time
import re
import math

mutex = Lock()

port = '/dev/ttyUSB1'

rteq = serial.Serial(port, 115200, timeout = 0.1)

radius = 0.2159

leftPat = re.compile("\$\d+\$")
rightPat = re.compile("#\d+#")

def callback(data):
	#totalVelocity = math.sqrt(math.pow(data.linear.x,2) + math.pow(data.linear.y,2) + math.pow(data.linear.z,2))
	#angular = math.sqrt(math.pow(data.angular.x,2) + math.pow(data.angular.y,2) + math.pow(data.angular.z,2))
	#leftSpeed = totalVelocity - (0.7874*angular)/2;
	#rightSpeed = totalVelocity + (0.7874*angular)/2;

	leftSpeed = data.linear.x - data.angular.z * 0.7874/2
        rightSpeed = data.linear.x + data.angular.z * 0.7874/2
	leftSpeed = leftSpeed/(radius * .010472)
	rightSpeed = rightSpeed/(radius * .010472)
	#leftSpeed = int(leftSpeed * 2)
	#rightSpeed = int(rightSpeed * 2)
	leftSpeed = (leftSpeed*1000)/(1155)
	rightSpeed = (rightSpeed * 1000)/(1155)

	print("Left speed " + str(leftSpeed) + " Right speed " + str(rightSpeed))    

	mutex.acquire()
	rteq.write("!G 1 "+ str(leftSpeed) +"\r!G 2 " + str(rightSpeed) + "\r")
	mutex.release()

def wheelPublisher():
    left = rospy.Publisher('left_wheel',Int32, queue_size = 10)
    right = rospy.Publisher('right_wheel',Int32, queue_size = 10)
    rospy.init_node('speedPublisher', anonymous = True)
    
    rospy.Subscriber('cmd_vel',Twist, callback)
    rate = rospy.Rate(100)
    
    while not rospy.is_shutdown():

        speedLeft = Int32()
        speedRight = Int32()
        mutex.acquire()
        byte = rteq.readline()
        rightCurrentSpeed = rightPat.search(byte)
        leftCurrentSpeed = leftPat.search(byte)

        if(leftCurrentSpeed != None):
            leftCurrentSpeed = leftCurrentSpeed.group()
            leftOut = leftCurrentSpeed[1:len(leftCurrentSpeed) - 1]
            speedLeft.data = int(leftOut)
            speedLeft.data = speedLeft.data * radius * 0.10472
        if(rightCurrentSpeed != None):
            rightCurrentSpeed = rightCurrentSpeed.group()
            rightOut = rightCurrentSpeed[1:len(rightCurrentSpeed)-1]
            speedRight.data = int(rightOut)
            speedRight.data = speedRight.data * radius * 0.10472

        mutex.release()
        left.publish(speedLeft)
        right.publish(speedRight)

        rate.sleep()


if __name__ == '__main__':
    wheelPublisher()

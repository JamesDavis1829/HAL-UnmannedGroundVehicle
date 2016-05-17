#!/usr/bin/env python
import rospy
import cv2
import roslib
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def callback(data):
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(data,"bgr8")
    cv2.imshow("image",cv_image)
    cv2.waitKey(1)

def cvListener():
    rospy.init_node('cvlistener', anonymous = True)
    rospy.Subscriber('open_cv_image2', Image, callback)
    rospy.spin()


if __name__ == '__main__':
    cvListener()
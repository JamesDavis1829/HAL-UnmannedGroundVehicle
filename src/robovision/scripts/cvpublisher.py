#!/usr/bin/env python
import rospy
import cv2
import roslib
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


def cvTalker():
    pub = rospy.Publisher('open_cv_image2',Image, queue_size = 10)
    rospy.init_node('cvTalker',anonymous = True)
    rate = rospy.Rate(20)
    cap = cv2.VideoCapture(0)
    while not rospy.is_shutdown():
        #get an opencv image
        ret, frame = cap.read()
        bridge = CvBridge()
        pubImage = bridge.cv2_to_imgmsg(frame, "bgr8")
        pub.publish(pubImage)
        rate.sleep()

if __name__ == '__main__':
    try:
        cvTalker()
    except rospy.ROSInterruptException:
        pass

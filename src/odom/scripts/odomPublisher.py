#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry
import tf
from geometry_msgs.msg import Point, Quaternion, TransformStamped
from std_msgs.msg import Int32
import math

leftV = 0
rightV = 0
l = 0.8128

def leftCB(data):
    leftV = data.data

def rightCB(data):
    rightV = data.data;

def odom_publisher():
    rospy.Subscriber('left_wheel',Int32,leftCB)
    rospy.Subscriber('right_wheel',Int32, rightCB)

    rospy.init_node('odometr_ppublisher', anonymous = True)
    odom_pub = rospy.Publisher('odom',Odometry,queue_size = 50)
    odom_broadcaster = tf.TransformBroadcaster()

    rate = rospy.Rate(20)

    x = 0
    y = 0
    th = 0

    vx = 0
    vy = 0
    vth = 0

    current_time = prev_time = rospy.Time.now()

    while not rospy.is_shutdown():
        current_time = rospy.Time.now()

        vx = (0.5)*rightV + (0.5)*leftV
        vth = (-1/l)*rightV + (1/l)*leftV

        dt = (current_time - prev_time).to_sec()
        delta_x =(vx*math.cos(th) - vy*math.cos(th))*dt
        delta_y =(vy*math.sin(th) - vy*math.sin(th))*dt
        delta_th = vth * dt

	x += delta_x
	y += delta_y
	th += delta_th

        odom_quat = tf.transformations.quaternion_from_euler(0,0,th)

        odom_trans = TransformStamped()
        odom_trans.header.stamp = current_time;
        odom_trans.header.frame_id = "odom"
        odom_trans.child_frame_id = "base_link"

        odom_trans.transform.translation.x = x
        odom_trans.transform.translation.y = y
        odom_trans.transform.translation.z = 0
        odom_trans.transform.rotation = odom_quat

        transform = (x,y,0)
        rot = (odom_quat[0],odom_quat[1],odom_quat[2],odom_quat[3])
        odom_broadcaster.sendTransform(transform,rot,current_time,"base_link","odom")

        odom = Odometry()
        odom.header.stamp = current_time
        odom.header.frame_id = "odom"

        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = 0

	odom.pose.pose.orientation.x = odom_quat[0]
	odom.pose.pose.orientation.y = odom_quat[1]
	odom.pose.pose.orientation.z = odom_quat[2]
	odom.pose.pose.orientation.w = odom_quat[3]

        odom.child_frame_id = "base_link"
        odom.twist.twist.linear.x = vx
        odom.twist.twist.linear.y = vy
        odom.twist.twist.linear.z = vth

        odom_pub.publish(odom)

        last_time = current_time
        rate.sleep()

if __name__ == '__main__':
    odom_publisher()
    

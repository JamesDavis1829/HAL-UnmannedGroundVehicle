#!/usr/bin/env python
import rospy
import tf

def tf_broadcaster():
    rospy.init_node('robot_tf_publisher',anonymous = True)

    rate = rospy.Rate(20)

    broadcaster = tf.TransformBroadcaster()

    while not rospy.is_shutdown():
	broadcaster.sendTransform((0.26035,0,0.18415),(0,0,0,1),rospy.Time.now(),"base_laser","base_link")
        rate.sleep()

if __name__ == '__main__':
    tf_broadcaster()

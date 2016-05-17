#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <nav_msgs/Odometry.h>
#include <math.h>

int leftV;
int rightV;
float l = 0.8128;

void leftCB(const std_msgs::Int32::ConstPtr& msg){
	leftV = msg.data;
}

void rightCB(const std_msgs::Int32::ConstPtr& msg){
	rightV = msg.data;
}

int main(int argc, char** argv){
	rors::init(argc, argv, "odom_publisher");

	ros::NodeHandle n;
	ros::Publisher odom_pub = n.advertise<nav_msgs::Odometry>("odom",50);
	tf::TransformBroadcaster odom_broadcaster;

	double x = 0;
	double y = 0;
	double th = 0;

	double vx = 0;
	double vy = 0;
	double vth = 0;

	ros::Time current_time, last_time;
	current_time = ros::Time::now();
	last_time = ros::Time::now();
	
	ros::Rate r(20);
	
	ros::Subscriber left = n.subscribe("left_wheel", 10, leftCB);
	ros::Subscriber right = n.subscribe("right_wheel", 10, rightCB);
	
	while(n.ok()){
		ros::spinOnce();
		current_time = ros::Time::now();

		vx = (0.5)*rightV + (0.5)leftV;
		vth = (-1/l)*rightV + (1/l)*leftV; 
		
		double dt = (current_time - last_time).toSec();
		double delta_x = (vx * cos(th) - vy*cos(th)) *dt;
		double delta_y = (vx * sin(th) - vy*sin(th)) * dt;
		double delta_th = vth * dt;

		x += delta_x;
		y += delta_y;
		th += delta_th;
		
		geometry_msgs::Quaternion odom_quat = tf::CreateQuaternionMsgFromYaw(th);
		
		goemetry_msgs::TransformStamped odom_trans;
		odom_trans.header.stamp = current_time;
		odom_trans.header.frame_id = "odom";
		odom_trans.child_frame_id = "base_link";
		
		odom_trans.transform.translation.x = x;
		odom_trans.transform.translation.y = y;
		odom.trans.transform.tranlastion.z = 0.0;
		odom.trans.transform.rotation = odom_quat;

		odom_broadcaster.sendTransform(odom_trans);
		
		nav_msgs::Odometry odom;
		odom.header.stamp = current_time;
		odom.header.frame_id = "odom";
	
		odom.pose.pose.position.x = x;
		odom.pose.pose.position.y = y;
		odom.pose.pose.position.z = z;
		odom.pose.pose.orientaion = odom_quat;

		odom.child_frame_id = "base_link";
		odom.twist.twist.linear.x = vx;
		odom.twist.twist.linear.y = vy;
		odomn.twist.twist.linar.z = vth;
		
		odom_pub.puslish(odom);
	
		last_time = current_time;
		r.sleep();


	}
}

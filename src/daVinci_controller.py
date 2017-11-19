#!/usr/bin/env python

import rospy
import cv2
from std_msgs.msg import Float64
from sensor_msgs.msg import Joy
from math import pi

setup1_angle = Float64()
setup2_angle = Float64()
setup3_angle = Float64()

outer_yaw = Float64()
outer_pitch = Float64()

def ds4_callback(controller):
	outer_yaw.data = -controller.axes[3]
	outer_pitch.data = -controller.axes[4]

def slider_callback(self):
	setup1_angle.data = cv2.getTrackbarPos('Setup 1 (deg): ', 'Setup Joints') * pi / 180.0
	setup2_angle.data = cv2.getTrackbarPos('Setup 2 (deg): ', 'Setup Joints') * pi / 180.0
	setup3_angle.data = cv2.getTrackbarPos('Setup 3 (deg): ', 'Setup Joints') * pi / 180.0

rospy.init_node('daVinci_controller', anonymous=True)

rospy.Subscriber('/joy', Joy, ds4_callback)

setup1_pub = rospy.Publisher('/daVinci/setup1_position_controller/command', Float64, queue_size=10)
setup2_pub = rospy.Publisher('/daVinci/setup2_position_controller/command', Float64, queue_size=10)
setup3_pub = rospy.Publisher('/daVinci/setup3_position_controller/command', Float64, queue_size=10)

outer_yaw_pub = rospy.Publisher('/daVinci/outer_yaw_position_controller/command', Float64, queue_size=10)
outer_pitch_pub = rospy.Publisher('/daVinci/outer_pitch_position_controller/command', Float64, queue_size=10)

#Using sliders to control the setup joints
cv2.namedWindow('Setup Joints', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Setup 1 (deg): ', 'Setup Joints', -180, 180, slider_callback)
cv2.createTrackbar('Setup 2 (deg): ', 'Setup Joints', -90, 90, slider_callback)
cv2.createTrackbar('Setup 3 (deg): ', 'Setup Joints', -90, 90, slider_callback)

cv2.setTrackbarPos('Setup 1 (deg): ', 'Setup Joints', 0)
cv2.setTrackbarPos('Setup 2 (deg): ', 'Setup Joints', 0)
cv2.setTrackbarPos('Setup 3 (deg): ', 'Setup Joints', 0)

while not rospy.is_shutdown():
	setup1_pub.publish(setup1_angle)
	setup2_pub.publish(setup2_angle)
	setup3_pub.publish(setup3_angle)

	outer_yaw_pub.publish(outer_yaw)
	outer_pitch_pub.publish(outer_pitch)

	key = cv2.waitKey(1) & 0xFF
	if key == 27:
		break

cv2.destroyAllWindows()
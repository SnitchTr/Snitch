#!/usr/bin/env python3


import serial
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32

class ROS2ArduinoNode(object):
    def __init__(self):
        rospy.loginfo("arduino post started")
        self.ser = serial.Serial('/dev/ttyACM0',baudrate = 9600, timeout=10)
        rospy.Subscriber("ros2arduino", Int32, self.serial_publish)

    def serial_publish(self, msg):
        rawmsg = msg.data
        send =(rawmsg).to_bytes(2, byteorder='big')
        rospy.loginfo(send)
        self.ser.write(send)

if __name__ == "__main__":
    rospy.init_node("ROS2Arduino_node")
    node = ROS2ArduinoNode()
    rospy.spin()

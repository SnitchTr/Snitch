#!/usr/bin/env python3

import serial
import rospy
from std_msgs.msg import Int16

class ArduinoPublisherNode:
    def __init__(self):
        rospy.loginfo("Starting arduino_publisher")
        self.ser = serial.Serial('/dev/ttyACM0',baudrate = 9600, timeout=10)
        # create a publisher object to send data
        self.pub = rospy.Publisher("Arduino", Int16, queue_size=10)

        PUBLISH_RATE = 10.0 # 10 Hz
        # create a timer that calls the timer_callback function at
        # the specified rate
        rospy.Timer(rospy.Duration(1.0/PUBLISH_RATE), self.arduino_read)

    def arduino_read(self, event):
        num = self.ser.read(2)
        num=int.from_bytes(num,'big')
        self.pub.publish(num)


if __name__ == "__main__":
    rospy.init_node("arduino_publisher")
    node = ArduinoPublisherNode()
    rospy.spin()

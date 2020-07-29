#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from pyPS4Controller.controller import Controller,Event
import shutil
import os

class MyController(Controller):

    def on_x_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('x_press')
        rospy.Publisher("x", String, queue_size=10).publish('1')
    def on_x_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('x_release')
    def on_triangle_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('triangle_press')
    def on_triangle_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('triangle_release')
    def on_circle_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('circle_press')
    def on_circle_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('circle_release')
    def on_square_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('square_press')
    def on_square_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('square_release')
    def on_L1_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('L1_press')
    def on_L1_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('L1_release')
    def on_L2_press(self,value):
        datastr = 'L2_press ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_L2_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('L2_release')
    def on_R1_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('R1_press')
    def on_R1_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('R1_release')
    def on_R2_press(self,value):
        datastr = 'R2_press ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_R2_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('R2_release')
    def on_up_arrow_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('up_arrow_press')
    def on_up_down_arrow_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('up_down_arrow_release')
    def on_down_arrow_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('down_arrow_press')
    def on_left_arrow_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('left_arrow_press')
    def on_left_right_arrow_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('left_right_arrow_release')
    def on_right_arrow_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('right_arrow_press')
    def on_L3_up(self,value):
        datastr = 'L3_up ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_L3_down(self,value):
        datastr = 'L3_down ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_L3_left(self,value):
        datastr = 'L3_left ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_L3_right(self,value):
        datastr = 'L3_right ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_L3_at_rest (self):
        rospy.Publisher("input", String, queue_size=10).publish('L3_at_rest') # L3 joystick is at rest after the joystick was moved and let go off
    def on_L3_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('L3_press')  # L3 joystick is clicked. This event is only detected when connecting without ds4drv
    def on_L3_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('L3_release') # L3 joystick is released after the click. This event is only detected when connecting without ds4drv
    def on_R3_up(self,value):
        datastr = 'R3_up ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_R3_down(self,value):
        datastr = 'R3_down ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_R3_left(self,value):
        datastr = 'R3_left ' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_R3_right(self,value):
        datastr = 'R3_right' + str(value)
        rospy.Publisher("input", String, queue_size=10).publish(datastr)
    def on_R3_at_rest(self):
        rospy.Publisher("input", String, queue_size=10).publish('R3_at_rest') # R3 joystick is at rest after the joystick was moved and let go off
    def on_R3_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('R3_press') #R3 joystick is clicked. This event is only detected when connecting without ds4drv
    def on_R3_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('R3_release')  # R3 joystick is released after the click. This event is only detected when connecting without ds4drv
    def on_options_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('options_press')
    def on_options_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('options_release')
    def on_share_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('share_press')
        rospy.Publisher("off", String, queue_size=10).publish('1')
        exit()  # this event is only detected when connecting without ds4drv
    def on_share_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('share_release')  # this event is only detected when connecting without ds4drv
    def on_playstation_button_press(self):
        rospy.Publisher("input", String, queue_size=10).publish('playstation_button_press')  # this event is only detected when connecting without ds4drv
    def on_playstation_button_release(self):
        rospy.Publisher("input", String, queue_size=10).publish('playstation_button_release')  # this event is only detected when connecting without ds4drv

class MyEventDefinition(Event):


    def x_pressed(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 1

    def x_released(self):
        return self.button_id == 0 and self.button_type == 1 and self.value == 0

    def circle_pressed(self):
        return self.button_id == 1 and self.button_type == 1 and self.value == 1

    def circle_released(self):
        return self.button_id == 1 and self.button_type == 1 and self.value == 0

    def triangle_pressed(self):
        return self.button_id == 2 and self.button_type == 1 and self.value == 1

    def triangle_released(self):
        return self.button_id == 2 and self.button_type == 1 and self.value == 0

    def square_pressed(self):
        return self.button_id == 3 and self.button_type == 1 and self.value == 1

    def square_released(self):
        return self.button_id == 3 and self.button_type == 1 and self.value == 0
class ControllerNode(object):
    counter = 0
    def __init__(self):
        rospy.loginfo("Strating Input_Publisher")



        rospy.loginfo('yep')
        rospy.Publisher("input", String, queue_size=10).publish('lul')
        controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False, event_definition=MyEventDefinition)
        controller.listen()



if __name__ == "__main__":
    rospy.init_node("number_publisher")
    node = ControllerNode()
    rospy.spin()

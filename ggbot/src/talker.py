#!/usr/bin/python

import rospy
from ggbot.msg import ggbot_motor
import sys, select, termios, tty



class talker:
    def __init__(self):
        self.ros_init()
        while not rospy.is_shutdown():
            self.key_to_board()

    def ros_init(self):
        self.motor_control = ggbot_motor()
        rospy.init_node('talker')   
        self.speed_angle_pub = rospy.Publisher('ggbot_motor', ggbot_motor, queue_size=10)
        rate = rospy.Rate(10)

    def key_to_board(self):
        settings=termios.tcgetattr(sys.stdin)
        input_str=self.getKey()
        self.transfer_speed_angle(input_str)
        # self.motor_control = self.xycar_motor()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    def getKey(self): #key input terminal
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [],0.1)
        settings=termios.tcgetattr(sys.stdin)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key

    def transfer_speed_angle(self, alpha):
        if (alpha == 'w'):
            speed=3
            angle=0
        elif (alpha == 's'):
            speed=0
            angle=0
        elif (alpha == 'q'):
            speed=3
            angle=-50
        elif (alpha == 'e'):
            speed=3
            angle=50
        elif (alpha == 'z'):
            speed=-3
            angle=-50
        elif (alpha == 'c'):
            speed=-3
            angle=50   
        elif (alpha == 'x'):
            speed=-3
            angle=0
        else:
            speed=0
            angle=0

        self.motor_pub(angle,speed)

    def motor_pub(self, angle, speed):
        # rospy.loginfo("%d %d",speed, angle)
        self.motor_control.angle = angle
        self.motor_control.speed = speed
        # rospy.loginfo(motor_control)
        self.speed_angle_pub.publish(self.motor_control)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

 
#!/usr/bin/env python2.7

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from math import radians, degrees, pi, sin, cos
from actionlib_msgs.msg import *
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
from copy import deepcopy
import tf
import numpy as np
import time
from std_msgs.msg import Float32MultiArray, Int16


def callback(msg):
    global current_odom
    current_odom.header.stamp = rospy.Time.now()

def callbackRoom(data):
    arr_room = []
    arr_room = data.data
    goal_def(arr_room)

class GoalPose:
    x = 0.
    y = 0.
    theta = 0.
    z = 0.
    w = 0.

def move_to(goal_point):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.orientation.x = 0
    goal.target_pose.pose.orientation.y = 0
    goal.target_pose.pose.orientation.z = goal_point.z
    goal.target_pose.pose.orientation.w = goal_point.w

    goal.target_pose.pose.position.x = goal_point.x
    goal.target_pose.pose.position.y = goal_point.y
    goal.target_pose.pose.position.z = 0

    # print(goal)
    ac.send_goal(goal)

def goal_def(arr_room):
    goal_test = GoalPose()
    error = 0.1

    for room in arr_room:
        if room == 301:
            rospy.loginfo("301")
            # goal_test.x = 1.79794210424
            # goal_test.y = 0.0
            goal_test.x = 5.41735
            goal_test.y = -0.7224544
            goal_test.z = 0.657537242689
            goal_test.w = 0.753422042733
        elif room == 302:
            rospy.loginfo("302")
            goal_test.x = 1.75060760178
            goal_test.y = -0.279016830127
            goal_test.z = 0.657537242689
            goal_test.w = 0.753422042733
        elif room == 303:
            rospy.loginfo("303")
            goal_test.x = -1.73096152587
            goal_test.y = 0.651883785386
            goal_test.z = 0.213383708578
            goal_test.w = 0.976968478788
        elif room == 304:
            rospy.loginfo("304")
            goal_test.x = 1.75060760178
            goal_test.y = -0.279016830127
            goal_test.z = 0.657537242689
            goal_test.w = 0.753422042733
        
        move_to(goal_test)

        while((abs(current_odom.pose.pose.position.x - goal_test.x) > error) or (abs(current_odom.pose.pose.position.y - goal_test.y) > error)):
            hi = 1
        pub(1)
        rospy.sleep(6)
        
        
        





if __name__=='__main__':
    current_odom = PoseWithCovarianceStamped()
    rospy.init_node('room_listener')
    # odom_sub = rospy.Subscriber('/odom', Odometry, callback)
    odom_sub = rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, callback)
    tu_sub = rospy.Subscriber('room_info', Float32MultiArray, callbackRoom)
    ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    pub = rospy.Publisher('chatter', Int16, queue_size=10)
    ac.wait_for_server() # !!!!!!!!!!!!!!!!!!!!!!!!!!!

    rospy.spin()
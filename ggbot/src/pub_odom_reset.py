#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty



def no_name():
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
      # nonamed=""
      pub.publish()

      rate.sleep()  
if __name__ == '__main__': 
  try:
      rospy.init_node('pub_odom_reset')
      pub = rospy.Publisher('vesc_to_odom_node/reset_odometry', Empty, queue_size=1)
      no_name()

      
  except rospy.ROSInterruptException:
    pass
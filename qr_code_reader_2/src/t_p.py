#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray
import pyzbar.pyzbar as pyzbar
import cv2
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

#-*- coding:utf-8 -*-

cap = cv2.VideoCapture(0)

rospy.init_node('t_p')
tu_pub = rospy.Publisher('room_info', Float32MultiArray, queue_size=10)
rate=rospy.Rate(2)

i = 0
j = 0
toggle = 0
rem = ""
rem_ = ""
toggle2 = 0
arr_room = Float32MultiArray()
arr_room.data = []
while(cap.isOpened()):
  ret, img = cap.read()

  if not ret:
    continue

  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
     
  decoded = pyzbar.decode(gray)

  for d in decoded: 
    x, y, w, h = d.rect

    barcode_data = d.data.decode("utf-8")
    barcode_type = d.type

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    text = '%s (%s)' % (barcode_data, barcode_type)
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    rem_ = rem
    rem = barcode_data
    if toggle2==0:
      rem_= barcode_data
      toggle2=1
    if toggle==0:
      barcode_data_ = str(barcode_data)
      int_bada = int(barcode_data_)
      arr_room.data.append(int_bada)
      toggle=1
      rospy.loginfo(arr_room)
      j += 1

    if rem_ != rem:
	    toggle=0
    

  cv2.imshow('img', img)
  
  if j == 3:
    rospy.loginfo("gogo!")
    tu_pub.publish(arr_room)
    j = 0


cap.release()
cv2.destroyAllWindows()

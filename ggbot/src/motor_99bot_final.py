#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy, rospkg
import time
import serial
import threading
from ackermann_msgs.msg import AckermannDriveStamped
from ggbot.msg import ggbot_motor
from sensor_msgs.msg import LaserScan
import sys
import os
import signal

def signal_handler(sig, frame):
    import time
    time.sleep(3)
    os.system('killall -9 python rosout')  # 터미널 창에 입력하기
    sys.exit(0) # 파이썬 코드 즉시 중단s

signal.signal(signal.SIGINT, signal_handler) # 잘모르겠으니 알아서 찾으셈

class motor:
    def __init__(self): # 초기화를 위한 함수, 맨 처음 호출, 데이터의 초기 실시
        self.ros_init()
        self.set_parameter()
        rospy.spin()

    def set_parameter(self): # motor_type에 따른 motor_controller의 리스트 변화
        motor_controller = [0, 0, 0.0068, 0, 0, 0.08, 0, None, self.auto_drive_vesc]

        self.angle_weight = motor_controller[2] #0.0068
        self.angle_bias_1 = motor_controller[0] #0
        self.angle_bias_2 = motor_controller[1]
        self.speed_weight = motor_controller[5]
        self.speed_bias_1 = motor_controller[3]
        self.speed_bias_2 = motor_controller[4]
        self.Angle = motor_controller[6]
        self.Speed = motor_controller[6]
        self.seridev = motor_controller[7]
        self.auto_drive = motor_controller[8] #self.auto_drive_vesc
        self.angle_offset = 0.0
        self.last_speed = 0.0
        self.g_chk_time = 0
        self.change_vector_term = 0.05

    def ros_init(self):
        rospy.init_node('motor_99bot_final')
        rospy.Subscriber("/ggbot_motor", ggbot_motor, self.callback, queue_size=1) # xycar_motor 토픽값을 받음
        self.angle_offset = rospy.get_param("~angle_offset") # angle의 초기값을 잡아줌(launch 파일에 초기 값 0으로 설정)

        self.ack_msg = AckermannDriveStamped()
        self.ack_msg.header.frame_id = '' # frame_id의 형태는 string
        self.ackerm_publisher = rospy.Publisher('ackermann_cmd', AckermannDriveStamped, queue_size=1) # AckermannDriveStamped의 저장 된 값 보냄

    def auto_drive_vesc(self, steer_val, car_run_speed):
        self.ack_msg.header.stamp = rospy.Time.now()
        self.ack_msg.drive.steering_angle = -steer_val

        if (self.last_speed > 0) and (car_run_speed < 0): # 앞으로 가고 있는 상태에서 뒤로 가게 만들 때
            self.ack_msg.drive.speed = -50
            self.ackerm_publisher.publish(self.ack_msg) 
            time.sleep(self.change_vector_term) # 0.05초의 여유
            for _ in range(5): # 5번 실행
                self.ack_msg.drive.speed = 0
                self.ackerm_publisher.publish(self.ack_msg)
            time.sleep(self.change_vector_term)

        self.ack_msg.drive.speed = car_run_speed
        self.ackerm_publisher.publish(self.ack_msg)
        self.last_speed = car_run_speed
    
    def callback(self, data):

        data.angle = max(-50, min(data.angle, 50)) # 각도 -50~50까지의 최소 최대 범위 설정
        data.speed = max(-50, min(data.speed, 50)) # 속도 -50~50까지의 최소 최대 범위 설정

        Angle = (((float(data.angle + self.angle_offset) + self.angle_bias_1) * self.angle_weight)) + self.angle_bias_2 # 자기들 마음대로 계산
        Speed = ((float(data.speed) + self.speed_bias_1) * self.speed_weight) + self.speed_bias_2 # 

        self.auto_drive(Angle, Speed)


    # def calculate(self, data):
    #     data.angle = max(-50, min(data.angle, 50)) # 각도 -50~50까지의 최소 최대 범위 설정
    #     data.speed = max(-50, min(data.speed, 50)) # 속도 -50~50까지의 최소 최대 범위 설정

    #     Angle = (((float(data.angle + self.angle_offset) + self.angle_bias_1) * self.angle_weight)) + self.angle_bias_2 # 자기들 마음대로 계산
    #     Speed = ((float(data.speed) + self.speed_bias_1) * self.speed_weight) + self.speed_bias_2 # 

    #     self.auto_drive(Angle, Speed)
        
if __name__ == '__main__':
    m = motor()


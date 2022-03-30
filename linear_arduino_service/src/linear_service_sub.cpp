#include "ros/ros.h"
#include "linear_arduino_service/srvTutorial.h"
#include "std_msgs/Int16.h"

int test_msg;

void messageCb( const std_msgs::Int16& test){
  ros::NodeHandle nh;						// 노드 핸들 선

  ros::ServiceClient client = nh.serviceClient<linear_arduino_service::srvTutorial>("ard_cli");
  linear_arduino_service::srvTutorial srv;
  test_msg = test.data;   // blink the led
  ROS_INFO("%d", test_msg);
  if(test_msg == 1){ 

    ROS_INFO("ready");

    srv.request.a = 1;
    
    if(client.call(srv))
    {
      ROS_INFO("good");
    }
    ROS_INFO("not_yet");
  }
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "linear_service");		// 노드 초기화
  ros::NodeHandle nh;						// 노드 핸들 선

  ros::Subscriber sub = nh.subscribe("chatter", 100, &messageCb);

  // ros::ServiceClient client = nh.serviceClient<linear_arduino_service::srvTutorial>("ard_cli");
  // linear_arduino_service::srvTutorial srv;

  // if(test_msg == 1){ 

  //   ROS_INFO("ready");

  //   srv.request.a = 1;
    
  //   if(client.call(srv))
  //   {
  //     ROS_INFO("good");
  //   }
  //   ROS_INFO("not_yet");
  // }
  ros::spin();

  return 0;
}

#include "ros/ros.h"
#include "linear_arduino_service/srvTutorial.h"

// 서비스 요청이 있을 경우. 아래의 처리를 수행
// 서비스 요청은 req, 서비스 응답은 res로 설
/*bool callback(linear_arduino_service::srvTutorial::Request  &req,
                linear_arduino_service::srvTutorial::Response &res) {
  // 서비스 요청시 받은 a, 서비스 응답 값에 저장
  res.result = req.a;
  return true;
}*/




int main(int argc, char **argv)
{
  ros::init(argc, argv, "linear_service");		// 노드 초기화
  ros::NodeHandle nh;						// 노드 핸들 선

  // 서비스 서버 선언, linear_arduino_service 패키지의 srvTutorial 서비스 파일을 이용한
  // 서비스 서버 service를 선언한다.
  // 서비스명은 ard_cli이며 서비스 요청이 있을때 
  // add라는 함수를 실행하라는 설정이다.
  ros::ServiceClient client = nh.serviceClient<linear_arduino_service::srvTutorial>("ard_cli");
  
  linear_arduino_service::srvTutorial srv;
  srv.request.a = 1;
  if(client.call(srv))
  {
    ROS_INFO("good");
  }
  
  ROS_INFO("not_yet");
  ros::spin();

  return 0;
}
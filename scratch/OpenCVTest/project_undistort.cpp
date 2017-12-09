#include <iostream>
#include <vector>

#include "opencv2/opencv.hpp"

namespace {

template<typename T>
void print_vec(const char* label, std::vector<T> vec) {
  std::cout << label << ": {" << std::endl;
  for (T p : vec) {
    std::cout << "  " << p << std::endl;
  }
  std::cout << "}" << std::endl;
}


template<typename modelType, typename projectionType>
void project_there_and_back() {
  cv::Matx33d K;
  K << 723.9511019397465, 0, 290.2217310941673, 0, 723.9511019397465, 228.3566819856588, 0, 0, 1;
  std::vector<double> D = {0.2927964391985431, -1.744373877741121, -0.009353810819805932, -0.01201654749997177, 2.592201724637305};

  cv::Vec3d R = {2.936310307609032, -0.1735420352203717, 0.308174160830372};
  cv::Vec3d T = {0.0188201075039665, 0.06541305259320686, 0.4263606991364847};

  std::vector<modelType> model_points;
  model_points.push_back({0.0, 0.0, 0.0});
  model_points.push_back({0.0, -0.0636, -0.0125});
  model_points.push_back({-0.0433, 0.0327, -0.026});
  model_points.push_back({0.0433, 0.0327, -0.026});
  model_points.push_back({-0.0289, -0.0289, -0.0241});
  model_points.push_back({0.0289, -0.0289, -0.0241});

  std::vector<projectionType> projected_points;


  ::print_vec<modelType>("Model (in)", model_points);

  cv::projectPoints(model_points, R, T, K, D, projected_points);

  ::print_vec<projectionType>("Proj", projected_points);

  cv::undistortPoints(projected_points, model_points, K, D, R);

  ::print_vec<modelType>("Model (out)", model_points);
}

}

int main(int argc, char** argv) {
  // cv::Point
  // No size
  // project_there_and_back<cv::Point, cv::Point>();  // Does not compile

  // 3 -> 2
  // project_there_and_back<cv::Point3f, cv::Point2f>();
  project_there_and_back<cv::Point3d, cv::Point2d>();
  // Both result in:
  // Assertion failed (mtype == type0 || (((((mtype) & ((512 - 1) << 3)) >> 3) + 1) == ((((type0) & ((512 - 1) << 3)) >> 3) + 1) && ((1 << type0) & fixedDepthMask) != 0)) in create
  // During call of undistortPoints

  // Same size
  // project_there_and_back<cv::Point3d, cv::Point3d>();
  // Assertion failed (mtype == type0 || (((((mtype) & ((512 - 1) << 3)) >> 3) + 1) == ((((type0) & ((512 - 1) << 3)) >> 3) + 1) && ((1 << type0) & fixedDepthMask) != 0)) in create
  // During call of projectPoints

  // cv::Vec
  // No size
  // project_there_and_back<cv::Vec, cv::Vec>();  // Does not compile

  // 3 -> 2
  // project_there_and_back<cv::Vec3f, cv::Vec2f>();
  // project_there_and_back<cv::Vec3d, cv::Vec2d>();
  // Assertion failed (mtype == type0 || (((((mtype) & ((512 - 1) << 3)) >> 3) + 1) == ((((type0) & ((512 - 1) << 3)) >> 3) + 1) && ((1 << type0) & fixedDepthMask) != 0)) in create
  // During call of undistortPoints

  // Same size
  // project_there_and_back<cv::Vec3d, cv::Vec3d>();
  // Assertion failed (mtype == type0 || (((((mtype) & ((512 - 1) << 3)) >> 3) + 1) == ((((type0) & ((512 - 1) << 3)) >> 3) + 1) && ((1 << type0) & fixedDepthMask) != 0)) in create
  // During call of projectPoints
}

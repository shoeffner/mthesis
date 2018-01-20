#include <chrono>
#include <iostream>
#include <numeric>

#include "dlib/opencv.h"
#include "opencv2/opencv.hpp"

#include "gaze/pipeline_steps.h"
#include "gaze/util/data.h"
#include "gaze/util/pipeline_utils.h"

double td(std::chrono::high_resolution_clock::time_point start, std::chrono::high_resolution_clock::time_point end) {
  return static_cast<double>(std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count());
}

int main(const int, const char** const) {
  // create list of image file names
  std::list<int> IMAGE_NUMS(120);
  std::iota(IMAGE_NUMS.begin(), IMAGE_NUMS.end(), 0);
  std::list<std::string> IMAGES;
  for (auto num : IMAGE_NUMS) {
    std::stringstream s;
    s << std::setfill('0') << std::setw(4) << num;
    IMAGES.push_back(s.str());
  }

  std::string IMAGE_PATH("../../../pexels_face_images/resized/");
  std::string ANNOTATIONS_PATH("../../../pexels_face_images/annotations/");
  std::string COMMA(", ");  // For crude csv parsing

  // Create pipeline
  gaze::pipeline::FaceLandmarks landmarks;
  gaze::pipeline::PupilLocalization pupil_localization;
  gaze::pipeline::EyeLike eye_like;
  gaze::pipeline::HeadPoseEstimation head_pose;
  gaze::pipeline::GazePointCalculation gpc;
  gaze::pipeline::GazeCapture gc;

  // Create stop watch
  std::chrono::high_resolution_clock::time_point start;
  std::chrono::high_resolution_clock::time_point end;

  // Write header
  std::cout << "id,landmarks_time,face_width,face_height,pupildetection_time,"
            << "eye_right_width,eye_right_height,target_right_x,target_right_y,gaze_right_x,gaze_right_y,"
            << "eye_left_width,eye_left_height,target_left_x,target_left_y,gaze_left_x,gaze_left_y,"
            << "eyelike_time,eyelike_right_x,eyelike_right_y,eyelike_left_x,eyelike_left_y,"
            << "headpose_time,"
            << "gazepoint_time,gazepoint_result_x,gazepoint_result_y,"
            << "gazecapture_time,gazecapture_result_x,gazecapture_result_y"
            << std::endl;

  int target_x[] = {0, 0};
  int target_y[] = {0, 0};
  for (auto FACE : IMAGES) {
    std::ifstream target_reader(ANNOTATIONS_PATH + FACE + ".csv");
    target_reader >> target_x[0] >> COMMA
                  >> target_y[0]
                  >> target_x[1] >> COMMA
                  >> target_y[1];
    if (target_x[0] + target_y[0] + target_x[1] + target_y[1] == 0) {
      continue;
    }


    // Create data object and load test image
    gaze::util::Data data;
    data.source_image = cv::imread(IMAGE_PATH + FACE + ".jpeg");
    dlib::assign_image(data.image, dlib::cv_image<dlib::bgr_pixel>(data.source_image));

    // Face landmarks
    start = std::chrono::high_resolution_clock::now();
    landmarks.process(data);
    end = std::chrono::high_resolution_clock::now();
    if (data.landmarks.num_parts() == 0) {
      continue;
    }
    std::cout << FACE << COMMA
              << td(start, end) << COMMA
              << data.landmarks.get_rect().width() << COMMA
              << data.landmarks.get_rect().height() << COMMA;

    std::vector<dlib::chip_details> details =
      gaze::util::get_eyes_chip_details(data.landmarks);

    // pupil localization
    start = std::chrono::high_resolution_clock::now();
    pupil_localization.process(data);
    end = std::chrono::high_resolution_clock::now();
    std::cout << td(start, end) << COMMA;
    for (int i = 0; i < 2; ++i) {
      std::cout << details[i].rect.width() << COMMA
                << details[i].rect.height() << COMMA
                << target_x[i] << COMMA
                << target_y[i] << COMMA
                << details[i].rect.left() + data.centers[i].x() << COMMA
                << details[i].rect.top() + data.centers[i].y() << COMMA;
    }

    start = std::chrono::high_resolution_clock::now();
    eye_like.process(data);
    end = std::chrono::high_resolution_clock::now();
    std::cout << td(start, end) << COMMA;
    for (int i = 0; i < 2; ++i) {
      std::cout << details[i].rect.left() + data.centers[i].x() << COMMA
                << details[i].rect.top() + data.centers[i].y() << COMMA;
    }

    // Head pose
    start = std::chrono::high_resolution_clock::now();
    head_pose.process(data);
    end = std::chrono::high_resolution_clock::now();
    std::cout << td(start, end) << COMMA;

    // Gaze point calculation
    start = std::chrono::high_resolution_clock::now();
    gpc.process(data);
    end = std::chrono::high_resolution_clock::now();
    std::cout << td(start, end) << COMMA
              << data.estimated_gaze_point[0] << COMMA
              << data.estimated_gaze_point[1] << COMMA;

    // Gaze capture
    start = std::chrono::high_resolution_clock::now();
    gc.process(data);
    end = std::chrono::high_resolution_clock::now();
    std::cout << td(start, end) << COMMA
              << data.estimated_gaze_point[0] << COMMA
              << data.estimated_gaze_point[1] << std::endl;
  }
}

#include <iostream>
#include <numeric>

#include "dlib/opencv.h"
#include "opencv2/opencv.hpp"

#include "gaze/pipeline_steps.h"
#include "gaze/util/data.h"
#include "gaze/util/pipeline_utils.h"


int main(const int, const char** const) {
  // create list of image file names
  std::list<int> IMAGE_NUMS(1521);
  std::iota(IMAGE_NUMS.begin(), IMAGE_NUMS.end(), 0);
  std::list<std::string> IMAGES;
  for (auto num : IMAGE_NUMS) {
    std::stringstream s;
    s << std::setfill('0') << std::setw(4) << num;
    IMAGES.push_back(s.str());
  }

  std::string IMAGE_PATH("bio/");
  std::string ANNOTATIONS_PATH("bio/");
  std::string COMMA(",");
  std::string C0("#LX");
  std::string C1("LY");
  std::string C2("RX");
  std::string C3("RY");

  // Create pipeline
  gaze::pipeline::FaceLandmarks landmarks;
  gaze::pipeline::PupilLocalization pupil_localization;
  gaze::pipeline::EyeLike eye_like;

  int target_x[] = {0, 0};
  int target_y[] = {0, 0};

  // Write header
  std::cout << "id,face_width,face_height,"
            << "eye_right_width,eye_right_height,target_right_x,target_right_y,gaze_right_x,gaze_right_y,"
            << "eye_left_width,eye_left_height,target_left_x,target_left_y,gaze_left_x,gaze_left_y,"
            << "eyelike_right_x,eyelike_right_y,eyelike_left_x,eyelike_left_y"
            << std::endl;

  for (auto FACE : IMAGES) {
    std::ifstream target_reader(ANNOTATIONS_PATH + "BioID_" + FACE + ".eye");
    target_reader >> C0 >> C1 >> C2 >> C3
                  >> target_x[1]
                  >> target_y[1]
                  >> target_x[0]
                  >> target_y[0];
    if (target_x[0] + target_y[0] + target_x[1] + target_y[1] == 0) {
      continue;
    }

    // Create data object and load test image
    gaze::util::Data data;
    data.source_image = cv::imread(IMAGE_PATH + "BioID_" + FACE + ".pgm");
    dlib::assign_image(data.image, dlib::cv_image<dlib::bgr_pixel>(data.source_image));

    // Face landmarks
    landmarks.process(data);
    if (data.landmarks.num_parts() == 0) {
      continue;
    }
    std::cout << FACE << COMMA
              << data.landmarks.get_rect().width() << COMMA
              << data.landmarks.get_rect().height() << COMMA;

    std::vector<dlib::chip_details> details =
      gaze::util::get_eyes_chip_details(data.landmarks);

    // pupil localization
    pupil_localization.process(data);
    for (int i = 0; i < 2; ++i) {
      std::cout << details[i].rect.width() << COMMA
                << details[i].rect.height() << COMMA
                << target_x[i] << COMMA
                << target_y[i] << COMMA
                << details[i].rect.left() + data.centers[i].x() << COMMA
                << details[i].rect.top() + data.centers[i].y() << COMMA;
    }

    eye_like.process(data);
    for (int i = 0; i < 2; ++i) {
      std::cout << details[i].rect.left() + data.centers[i].x() << COMMA
                << details[i].rect.top() + data.centers[i].y() << (i == 0 ? COMMA : "");
    }
    std::cout << std::endl;
  }
}

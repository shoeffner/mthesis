#include <iostream>
#include <memory>
#include <utility>

#include "gaze/gaze.h"

int main(const int, const char** const) {
  std::unique_ptr<gaze::GazeTracker> tracker(new gaze::GazeTracker("1"));
  for (int i = 0; i < 20; ++i) {
    std::pair<int, int> point = tracker->get_current_gaze_point();
    std::cout << point.first << ", " << point.second << std::endl;
  }
}

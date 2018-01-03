#include <iostream>
#include <utility>

#include "gaze/gaze.h"

int main(const int, const char** const) {
  gaze::GazeTracker* tracker = new gaze::GazeTracker("subject");
  for (int i = 0; i < 20; ++i) {
    std::pair<int, int> point = tracker->get_current_gaze_point();
    std::cout << point.first << ", " << point.second << std::endl;
  }
  delete tracker;
}

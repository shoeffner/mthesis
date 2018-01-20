cmake_minimum_required(VERSION 3.0)
project(gaze_evaluation VERSION 1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

find_package(dlib REQUIRED)
find_package(OpenCV REQUIRED)
find_package(itracker REQUIRED)
find_package(gaze REQUIRED)

link_directories(
    /usr/local/opt/openblas/lib
)

add_executable(bioid bioid.cpp)
target_link_libraries(bioid dlib::dlib gaze::gaze ${OpenCV_LIBRARIES})

add_executable(pexels pexels.cpp)
target_link_libraries(pexels itracker::itracker dlib::dlib gaze::gaze ${OpenCV_LIBRARIES})

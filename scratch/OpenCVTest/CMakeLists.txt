project(OpenCVTest)
cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 17)

find_package(OpenCV REQUIRED COMPONENTS core calib3d)
include_directories(
    ${OpenCV_INCLUDE_DIRS}
)
link_directories(
    ${OpenCV_LIBRARY_DIRS}
)

add_executable(project_undistort project_undistort.cpp)
target_link_libraries(project_undistort ${OpenCV_LIBS})

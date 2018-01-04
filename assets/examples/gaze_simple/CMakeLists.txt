cmake_minimum_required(VERSION 3.0)
project(gaze_simple VERSION 1 LANGUAGES CXX)
set(CMAKE_CXX_STANDARD 17)

find_package(dlib REQUIRED)
find_package(gaze REQUIRED)
find_package(OpenCV REQUIRED)

add_executable(${PROJECT_NAME} ${PROJECT_NAME}.cpp)
target_link_libraries(${PROJECT_NAME}
    dlib::dlib gaze::gaze ${OpenCV_LIBRARIES})

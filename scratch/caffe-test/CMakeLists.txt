project(caffe-test)
cmake_minimum_required(VERSION 3.10)
set(CMAKE_CXX_STANDARD 11)


find_package(OpenCV REQUIRED)
find_package(caffe REQUIRED)
find_package(BLAS REQUIRED)
find_package(Boost REQUIRED COMPONENTS system)

include_directories(
    ${OpenCV_INCLUDE_DIRS}
    ${caffe_INCLUDE_DIRS}
    ${BLAS_INCLUDE_DIRS}
    ${Boost_INCLUDE_DIRS}
    # Ugly hack, but how to find BLAS headers?
    /System/Library/Frameworks/Accelerate.framework/Versions/A/Frameworks/vecLib.framework/Versions/A/Headers
)
link_directories(
    ${OpenCV_LIBRARY_DIRS}
    /usr/local/Cellar/caffe/1.0/lib
    ${BLAS_LIBRARY_DIRS}
    ${Boost_LIBRARY_DIRS}
)

add_definitions(-DCPU_ONLY=1)

get_cmake_property(_variableNames VARIABLES)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()

add_executable(${PROJECT_NAME} ${PROJECT_NAME}.cpp)
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS} ${caffe_LIBS} ${caffe_LIBRARIES} ${BLAS_LIBRARIES} ${Boost_LIBRARIES} boost_system libcaffe.dylib glog)

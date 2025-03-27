textcmake_minimum_required(VERSION 3.10)
project(DeadlockToolkit)

set(CMAKE_CXX_STANDARD 11)

find_package(SFML COMPONENTS graphics window system REQUIRED)

include_directories(include)

add_executable(DeadlockToolkit src/main.cpp src/deadlock_detection.cpp src/deadlock_prevention.cpp src/visualization.cpp)
target_link_libraries(DeadlockToolkit sfml-graphics sfml-window sfml-system)
cmake_minimum_required(VERSION 3.16)
project(EmbededKalmanFilter C)
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -03")

include_directories(include)

add_library(kalman_static STATIC src/kalman.c)
add_executable(bench_kalman bench/main.c)
target_link_libraries(bench_kalman PRIVATE kalman_static)
cmake_minimum_required(VERSION 3.1)
project(test_package C)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

set(FONT_PATH "${CMAKE_CURRENT_LIST_DIR}/OpenSans-Bold.ttf" CACHE STRING "Path of font")

find_package(SDL2_ttf REQUIRED CONFIG)

add_executable(${PROJECT_NAME} test_package.c)
target_compile_definitions(${PROJECT_NAME} PRIVATE FONT_PATH="${FONT_PATH}")
target_link_libraries(${PROJECT_NAME} SDL2_ttf::SDL2_ttf)

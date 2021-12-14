cmake_minimum_required(VERSION 3.1)
project(test_package)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
if(${IMGUI_SFML_VERSION} VERSION_GREATER 2.3)
    add_compile_definitions(IMGUI_SFML_VERSION_GREATER_THAN_2_3)
endif()
add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS})

cmake_minimum_required(VERSION 2.8.9)
project (TestLibrary)

#Bring the headers, such as Student.h into the project
include_directories(include)

add_executable(TEST_STUDENT libtest.cpp)


#However, the file(GLOB...) allows for wildcard additions:
set(LIB_STUDENT_SOURCES "src/Student.cpp")

# add_dependencies(TEST_STUDENT LIB_STUDENT)
add_library(LIB_STUDENT SHARED ${LIB_STUDENT_SOURCES})
target_link_libraries(TEST_STUDENT LIB_STUDENT)



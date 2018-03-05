## hello world plug-in
cmake_minimum_required(VERSION 2.8)

## ensure out-of-source build
if("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")
    message(FATAL_ERROR "An out-of-source build is required. Please see the README.")
endif("${CMAKE_SOURCE_DIR}" STREQUAL "${CMAKE_BINARY_DIR}")

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -std=gnu99")

# should we use our own math functions?
option (SHADOW_PLUGIN
    "Compile as a shadow plugin" OFF) 

message("SHADOW_PLUGIN:" ${SHADOW_PLUGIN})

if (${SHADOW_PLUGIN} STREQUAL "ON") 
  ## we need to know where shadow is installed
  if("${SHADOW_ROOT}" STREQUAL "")
    set(SHADOW_ROOT "$ENV{HOME}/.shadow")
  endif("${SHADOW_ROOT}" STREQUAL "")
  if(EXISTS "${SHADOW_ROOT}")
    message(STATUS "SHADOW_ROOT = ${SHADOW_ROOT}")
  else()
    message(FATAL_ERROR "SHADOW_ROOT path does not exist: '${SHADOW_ROOT}'")
  endif()

  set(CMAKE_INSTALL_PREFIX "${SHADOW_ROOT}")

  if(EXISTS "${CMAKE_INSTALL_PREFIX}")
    message(STATUS "CMAKE_INSTALL_PREFIX = ${CMAKE_INSTALL_PREFIX}")
  else()
    message(FATAL_ERROR "CMAKE_INSTALL_PREFIX path does not exist: '${CMAKE_INSTALL_PREFIX}'")
  endif()

  ## we use cmake files from shadow
  set(CMAKE_MODULE_PATH "${SHADOW_ROOT}/share/cmake/Modules")
  if(EXISTS "${CMAKE_MODULE_PATH}")
    message(STATUS "CMAKE_MODULE_PATH = ${CMAKE_MODULE_PATH}")
  else()
    message(FATAL_ERROR "CMAKE_MODULE_PATH path does not exist: '${CMAKE_MODULE_PATH}'")
  endif()
  include_directories(${CMAKE_MODULE_PATH})
  include(ShadowTools)

  ## create and install a shared library that can plug into shadow
  add_shadow_plugin(shadow-plugin-hello hello.c)
  target_link_libraries(shadow-plugin-hello)
  install(TARGETS shadow-plugin-hello DESTINATION plugins)
  # add_executable(hello_plugin hello.c)
else (${SHADOW_PLUGIN} STREQUAL "ON") 
    add_executable(hello hello.c)
endif (${SHADOW_PLUGIN} STREQUAL "ON") 

#if (${SHADOW_PLUGIN} STREQUAL "OFF")
## create and install an executable that can run outside of shadow
#    add_executable(hello hello.c)
#endif (${SHADOW_PLUGIN} STREQUAL "NO")

cmake_minimum_required(VERSION 3.18...3.27)
project(hyperon_das_node)

set(CMAKE_VERBOSE_MAKEFILE ON)

set(DEV_MODULE Development.Module)

find_package(Python 3.10 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Detect the installed nanobind package and import it into CMake
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

include_directories(
  ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets
  ${CMAKE_CURRENT_SOURCE_DIR}/src/commons
  ${CMAKE_CURRENT_SOURCE_DIR}/src/atom_space_node)

file(GLOB_RECURSE headers
  ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets/*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/src/commons/*.h
  ${CMAKE_CURRENT_SOURCE_DIR}/src/atom_space_node/*.h)

nanobind_add_module(${PROJECT_NAME} MODULE bind.cc ${headers})


target_include_directories(${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets)

# .. and link it against the nanobind parts
target_link_libraries(
  hyperon_das_node PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets/libinternal.a
    ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets/libexternal.a

)

cmake_minimum_required(VERSION 3.18...3.27)
project(hyperon_das_node)

set(DEV_MODULE Development.Module)

find_package(Python 3.12 COMPONENTS Interpreter ${DEV_MODULE} REQUIRED)

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Detect the installed nanobind package and import it into CMake
execute_process(
  COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
  OUTPUT_STRIP_TRAILING_WHITESPACE OUTPUT_VARIABLE nanobind_ROOT)
find_package(nanobind CONFIG REQUIRED)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/commons)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/atom_space_node)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/bin/cache_node)

nanobind_add_module(hyperon_das_node MODULE bind.cc)

target_link_libraries(
  hyperon_das_node
  PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/bin/cache_node/libcache_node_lib.a
)

# # Build the core parts of nanobind once
# nanobind_build_library(nanobind SHARED)
#
# # Compile an extension library
# add_library(hyperon_das_node MODULE bind.cc)
#
# # .. and link it against the nanobind parts
# target_link_libraries(
#   hyperon_das_node PRIVATE nanobind 
#   ${CMAKE_CURRENT_SOURCE_DIR}/bin/cache_node/libcache_node_lib.a 
#   ${CMAKE_CURRENT_SOURCE_DIR}/bin/atom_space_node/libatom_space_node_lib.a
# )
#
# # .. enable size optimizations
# nanobind_opt_size(hyperon_das_node)
#
# # .. enable link time optimization
# nanobind_lto(hyperon_das_node)
#
# # .. set the default symbol visibility to 'hidden'
# nanobind_set_visibility(hyperon_das_node)
#
# # .. strip unneeded symbols and debug info from the binary (only active in release builds)
# nanobind_strip(hyperon_das_node)
#
# # .. disable the stack protector
# nanobind_disable_stack_protector(hyperon_das_node)
#
# # .. set the Python extension suffix
# nanobind_extension(hyperon_das_node)
#
# # .. set important compilation flags
# nanobind_compile_options(hyperon_das_node)
#
# # .. set important linker flags
# nanobind_link_options(hyperon_das_node)
#
# # Statically link against libstdc++/libgcc when targeting musllinux
# nanobind_musl_static_libcpp(hyperon_das_node)
#

# Set the minimum CMake version and policies for highest tested version
cmake_minimum_required(VERSION 3.15...3.27)

# Set up the project and ensure there is a working C++ compiler
project(hyperon_das_node LANGUAGES CXX)
set(EXTENSION_NAME "hyperon_das_node_ext")

# Warn if the user invokes CMake directly
if (NOT SKBUILD)
  message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build-core'.
  Running it directly will almost certainly not produce the desired
  result. If you are a user trying to install this package, use the
  command below, which will install all necessary build dependencies,
  compile the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to rerun the above
  after editing C++ files.")
endif()

# Try to import all Python components potentially needed by nanobind
find_package(Python 3.10
  REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

# Import nanobind through CMake's find_package mechanism
find_package(nanobind CONFIG REQUIRED)

set(DEV_MODULE Development.Module)

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

nanobind_add_module(
  ${EXTENSION_NAME} 
  # Target the stable ABI for Python 3.12+, which reduces
  # the number of binary wheels that must be built. This
  # does nothing on older Python versions
  STABLE_ABI

  # Build libnanobind statically and merge it into the
  # extension (which itself remains a shared library)
  #
  # If your project builds multiple extensions, you can
  # replace this flag by NB_SHARED to conserve space by
  # reusing a shared libnanobind across libraries
  NB_STATIC
  src/hyperon_das_node_ext.cc ${headers}
)


target_include_directories(${EXTENSION_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets)

# .. and link it against the nanobind parts
target_link_libraries(
  ${EXTENSION_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets/libinternal.a
    ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets/libexternal.a
    # ${CMAKE_CURRENT_SOURCE_DIR}/bazel_assets/libenvoy_api.a

)

# Install directive for scikit-build-core
install(TARGETS ${EXTENSION_NAME} LIBRARY DESTINATION ${PROJECT_NAME})

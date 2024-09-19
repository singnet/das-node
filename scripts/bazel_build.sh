#!/bin/bash

/opt/bazel/bazelisk build --jobs 6 --noenable_bzlmod //cache_node:cache_node_lib

##### Current workaround to build nanobind with CMake ######
# removes folder ../bin if exists
if [ -d "../bin" ]; then 
  rm -rf ../bin 
fi
if [ -d "../bazel_assets" ]; then 
  rm -rf ../bazel_assets 
fi

# Recreates folders
mkdir -p ../bin/
mkdir -p ../bazel_assets/

# Copy files
cp -r bazel-bin/* ../bin/
cp -r bazel-src/external/com_google_absl/absl/ ../bazel_assets/
cp -r bazel-src/external/com_github_grpc_grpc/include/grpcpp/ ../bazel_assets
cp -r bazel-src/external/com_github_grpc_grpc/include/grpc ../bazel_assets/
cp -r bazel-src/external/com_google_protobuf/src/google/ ../bazel_assets/
cp bazel-bin/external/com_github_singnet_das_proto/atom_space_node.pb.h ../bazel_assets/
cp bazel-bin/external/com_github_singnet_das_proto/atom_space_node.grpc.pb.h ../bazel_assets/
cp bazel-bin/external/com_github_singnet_das_proto/common.pb.h ../bazel_assets/
##### ---- ######

# /opt/bazel/bazelisk clean
# rm -f bazel-src bazel-out bazel-testlogs bazel-bin

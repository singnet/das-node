#!/bin/bash

/opt/bazel/bazelisk build --jobs 16 --noenable_bzlmod ...

##### Workaround to build nanobind with CMake ######
# removes folder if exists
if [ -d "../bazel_assets" ]; then 
  rm -rf ../bazel_assets 
fi

# Recreates folders
mkdir -p ../bazel_assets/

#Build external libs to bazel assets
ar rcs ../bazel_assets/libexternal.a \
  $(find bazel-bin/external/ -iname "*.o" -o -iname "*.lo" -o -iname "*.a")

#Build internal libs to bazel assets
# internal dirs of bazel-bin excliding external folder
ar rcs ../bazel_assets/libinternal.a \
  $(find bazel-bin/ -not -path 'bazel-bin/external/*' -iname "*o" -o -iname "*.lo" -o -iname "*.a")


# Copy files
cp -r bazel-src/external/com_github_grpc_grpc/include/grpc ../bazel_assets/
cp -r bazel-src/external/com_github_grpc_grpc/include/grpcpp/ ../bazel_assets
cp -r bazel-src/external/com_google_absl/absl/ ../bazel_assets/
cp -r bazel-src/external/com_google_protobuf/src/google/ ../bazel_assets/
cp bazel-bin/external/com_github_singnet_das_proto/atom_space_node.grpc.pb.h ../bazel_assets/
cp bazel-bin/external/com_github_singnet_das_proto/atom_space_node.pb.h ../bazel_assets/
cp bazel-bin/external/com_github_singnet_das_proto/common.pb.h ../bazel_assets/

##### ---- ######

# /opt/bazel/bazelisk clean
# rm -f bazel-src bazel-out bazel-testlogs bazel-bin

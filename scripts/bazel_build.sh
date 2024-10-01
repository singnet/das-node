#!/bin/bash

echo "===================================================================================================="
output="../bazel_assets"
/opt/bazel/bazelisk build --jobs 16 --noenable_bzlmod //:hyperon_das_node

##### Workaround to build nanobind with CMake ######
# removes folder if exists
if [ -d "$output" ]; then 
  rm -rf $output 
fi

# Recreates folders
mkdir -p $output/

#Build external libs to bazel assets
ar rcs $output/libexternal.a \
  $(find bazel-bin/external/ -iname "*.o" -o -iname "*.lo" -o -iname "*.a")

#Build internal libs to bazel assets
# internal dirs of bazel-bin excliding external folder
ar rcs $output/libinternal.a \
  $(find bazel-bin/ -not -path 'bazel-bin/external/*' -iname "*o" -o -iname "*.lo" -o -iname "*.a")

# Copy files
cp -r bazel-src/external/com_github_grpc_grpc/include/grpc $output/
cp -r bazel-src/external/com_github_grpc_grpc/include/grpcpp/ $output/
cp -r bazel-src/external/com_google_absl/absl/ $output/
cp -r bazel-src/external/com_google_protobuf/src/google/ $output/
cp bazel-bin/external/com_github_singnet_das_proto/atom_space_node.grpc.pb.h $output/
cp bazel-bin/external/com_github_singnet_das_proto/atom_space_node.pb.h $output/
cp bazel-bin/external/com_github_singnet_das_proto/common.pb.h $output/

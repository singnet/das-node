#!/bin/bash -x

echo "===================================================================================================="
output="../bazel_assets"
(( JOBS=$(nproc)/2 ))

/opt/bazel/bazelisk build --jobs ${JOBS} //:hyperon_das_node

[ "${?}" != "0" ] && exit 1

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
cp -r 'bazel-src/external/grpc+/include/grpc' $output/
cp -r 'bazel-src/external/grpc+/include/grpcpp' $output/
cp -r 'bazel-src/external/abseil-cpp+/absl' $output/
cp -r 'bazel-src/external/protobuf+/src/google' $output/

# TODO: Once das-proto is updated, update atom_space_node to distributed_algorithm_node

# cp 'bazel-bin/external/+_repo_rules+com_github_singnet_das_proto/distributed_algorithm_node.grpc.pb.h' $output/
# cp 'bazel-bin/external/+_repo_rules+com_github_singnet_das_proto/distributed_algorithm_node.pb.h' $output/
cp 'bazel-bin/external/+_repo_rules+com_github_singnet_das_proto/atom_space_node.grpc.pb.h' $output/
cp 'bazel-bin/external/+_repo_rules+com_github_singnet_das_proto/atom_space_node.pb.h' $output/
cp 'bazel-bin/external/+_repo_rules+com_github_singnet_das_proto/common.pb.h' $output/

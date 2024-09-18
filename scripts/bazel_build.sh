#!/bin/bash

/opt/bazel/bazelisk build --jobs 6 --noenable_bzlmod //src:atom_space_node_lib

##### Current workaround to build nanobind with CMake ######
cp -r bazel-bin/* ../bin/
cp -r /root/.cache/bazel/_bazel_root/ee73ef8bd6049ae309312492ee2f22da/external/com_google_absl/absl/ ../bazel_assets/
cp -r /root/.cache/bazel/_bazel_root/f400afec2d24eb3a6eb5cb42df4b7b24/external/com_github_grpc_grpc/include/grpcpp/ ../bazel_assets
cp -r /root/.cache/bazel/_bazel_root/f400afec2d24eb3a6eb5cb42df4b7b24/external/com_github_grpc_grpc/include/grpc ../bazel_assets/
cp /root/.cache/bazel/_bazel_root/f400afec2d24eb3a6eb5cb42df4b7b24/execroot/__main__/bazel-out/k8-fastbuild/bin/external/com_github_singnet_das_proto/atom_space_node.pb.h ../bazel_assets/
cp /root/.cache/bazel/_bazel_root/f400afec2d24eb3a6eb5cb42df4b7b24/execroot/__main__/bazel-out/k8-fastbuild/bin/external/com_github_singnet_das_proto/atom_space_node.grpc.pb.h ../bazel_assets/
cp -r /root/.cache/bazel/_bazel_root/f400afec2d24eb3a6eb5cb42df4b7b24/external/com_google_protobuf/src/google/ ../bazel_assets/
cp /root/.cache/bazel/_bazel_root/f400afec2d24eb3a6eb5cb42df4b7b24/execroot/__main__/bazel-out/k8-fastbuild/bin/external/com_github_singnet_das_proto/common.pb.h ../bazel_assets/
##### ---- ######

# /opt/bazel/bazelisk clean
# rm -f bazel-src bazel-out bazel-testlogs bazel-bin

#!/bin/bash

CONTAINER_NAME="das-node-build"

docker run \
  --rm \
  --name=$CONTAINER_NAME \
  --mount type=volume,source=bazel_cache,target=/root/.cache/bazel \
  --volume .:/opt/hyperon_das_node \
  --workdir /opt/hyperon_das_node/src \
  das-node-builder \
  ../scripts/cpp_build_cmd.sh

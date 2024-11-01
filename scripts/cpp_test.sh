#!/bin/bash

CONTAINER_NAME="das-node-cpp-test"

docker run \
  --rm \
  --name=$CONTAINER_NAME \
  --volume ./docker/volumes/bazel_cache:/root/.cache/bazel \
  --volume .:/opt/hyperon_das_node \
  --workdir /opt/hyperon_das_node/src \
  das-node-builder \
  ../scripts/cpp_test_cmd.sh

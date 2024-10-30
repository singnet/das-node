#!/bin/bash

# NOTE: We currently run the tests on the
# ubuntu:22.04 docker image, instead of the
# wheeler manylinux image.

CONTAINER_NAME="das-node-wheeler-test"

docker run \
  --rm \
  --name=$CONTAINER_NAME \
  --mount type=volume,source=bazel_cache,target=/root/.cache/bazel \
  --volume .:/opt/hyperon_das_node \
  --workdir /opt/hyperon_das_node \
  das-node-builder \
  ./scripts/wheeler_test_cmd.sh

#!/bin/bash

CONTAINER_NAME="das-node-build"

docker run \
    --name=$CONTAINER_NAME \
    --volume .:/opt/hyperon_das_node \
    --workdir /opt/hyperon_das_node/src \
    das-node-builder \
    ../scripts/bazel_build.sh

sleep 1
docker rm $CONTAINER_NAME

#!/bin/bash

CONTAINER_NAME="das-node-build"

docker run \
    -it \
    --name=$CONTAINER_NAME \
    --volume .:/opt/hyperon_das_node \
    --entrypoint /bin/bash \
    das-node-builder 
    # ../scripts/bazel_build.sh

sleep 1
docker rm $CONTAINER_NAME

#!/bin/bash

CONTAINER_NAME="das-node-build"

docker run \
    -it \
    --name=$CONTAINER_NAME \
    --volume .:/opt/das-node \
    --workdir /opt/das-node/src \
    --entrypoint /bin/bash \
    das-node-builder 
    # ../scripts/bazel_build.sh

sleep 1
docker rm $CONTAINER_NAME

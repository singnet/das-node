#!/bin/bash

CONTAINER_NAME="das-node-build"

mkdir -p bin
docker run \
    --name=$CONTAINER_NAME \
    --volume .:/opt/das-node \
    --workdir /opt/das-node/src \
    das-node-builder \
    ../scripts/bazel_test.sh

sleep 1
docker rm $CONTAINER_NAME

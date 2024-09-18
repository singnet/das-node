#!/bin/bash

docker buildx build -t das-node-builder --load -f docker/Dockerfile .
docker buildx build -t das-node-binder --load -f docker/Dockerfile.bind .

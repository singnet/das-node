#!/bin/bash

docker buildx build -t das-node-wheeler --load -f docker/Dockerfile.wheel .

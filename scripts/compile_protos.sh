#!/bin/bash

PROTOS=("echo" "common" "node")

for proto in ${PROTOS[@]}; do
    protoc -I/opt/proto --cpp_out=/opt/grpc /opt/proto/${proto}.proto
    cd /opt/grpc
    gcc -c ${proto}.pb.cc
done

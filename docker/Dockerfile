FROM ubuntu:22.04

ARG BASE_DIR="/opt"
ARG TMP_DIR="/tmp"

ARG DAS_NODE_DIR="${BASE_DIR}/hyperon_das_node"
ARG DATA_DIR="${BASE_DIR}/data"
ARG GRPC_DIR="${BASE_DIR}/grpc"
ARG PROTO_DIR="${BASE_DIR}/proto"
ARG BAZEL_DIR="${BASE_DIR}/bazel"
ARG THIRDPARTY="${BASE_DIR}/3rd-party"

RUN mkdir -p ${DAS_NODE_DIR} && mkdir -p ${DATA_DIR} && mkdir -p ${GRPC_DIR}\
  && mkdir -p ${BAZEL_DIR} && mkdir -p ${PROTO_DIR} && mkdir -p ${THIRDPARTY}

VOLUME ${DAS_NODE_DIR}

RUN apt-get update &&\
  apt-get install -y git build-essential autoconf libtool pkg-config curl gcc \
  protobuf-compiler libmbedcrypto7 python3 pip cmake python3 pip

RUN pip install --no-cache-dir nanobind==2.1.0

RUN cd ${GRPC_DIR} &&\
    git clone https://github.com/grpc/grpc &&\
    cd grpc &&\
    git submodule update --init

COPY assets/3rd-party.tgz ${THIRDPARTY}
RUN --mount=type=cache,target=/root/.cache/bazel cd ${THIRDPARTY} &&\
    tar xzvf 3rd-party.tgz &&\
    rm -f 3rd-party.tgz &&\
    mkdir -p ${DAS_NODE_DIR}}/src/3rd-party &&\
    ln -s ${THIRDPARTY} ${DAS_NODE_DIR}}/src/3rd-party &&\
    mv bazelisk ${BAZEL_DIR}
    
ENV CPLUS_INCLUDE_PATH="/opt/3rd-party/mbedcrypto/include/"

ENV CC=/usr/bin/gcc
RUN ln -s ${BAZEL_DIR}/bazelisk /usr/bin/bazel
RUN cd ${GRPC_DIR}/grpc &&\
    ${BAZEL_DIR}/bazelisk build :all

ADD https://raw.githubusercontent.com/singnet/das-query-engine/master/proto/common.proto ${PROTO_DIR}
ADD https://raw.githubusercontent.com/singnet/das-query-engine/master/proto/echo.proto ${PROTO_DIR}

WORKDIR "${DAS_NODE_DIR}"

#COPY source code and relevant info
COPY . .

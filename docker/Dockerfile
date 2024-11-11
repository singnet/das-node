FROM ubuntu:22.04

ARG BASE_DIR="/opt"
ARG TMP_DIR="/tmp"

ARG DAS_NODE_DIR="${BASE_DIR}/hyperon_das_node"
ARG DATA_DIR="${BASE_DIR}/data"
ARG GRPC_DIR="${BASE_DIR}/grpc"
ARG PROTO_DIR="${BASE_DIR}/proto"
ARG BAZEL_DIR="${BASE_DIR}/bazel"
ARG THIRDPARTY="${BASE_DIR}/3rd-party"


RUN mkdir -p ${DAS_NODE_DIR} ${DATA_DIR} ${GRPC_DIR} \ 
  ${BAZEL_DIR} ${PROTO_DIR} ${THIRDPARTY}

VOLUME ${DAS_NODE_DIR}

RUN apt-get update &&\
  apt-get install -y git build-essential autoconf libtool pkg-config curl gcc \
  protobuf-compiler libmbedcrypto7 python3 pip cmake make python3 pip libssl-dev

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

COPY deps/* ${THIRDPARTY}
RUN cd ${TMP_DIR} \
  && tar -xzf ${THIRDPARTY}/paho.mqtt.c.tar.gz \
  && cd paho.mqtt.c-1.3.9 \
  && cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_WITH_SSL=ON  -DPAHO_HIGH_PERFORMANCE=ON -DPAHO_BUILD_STATIC=ON \
  && cmake --build build/ --target install
 

RUN cd ${TMP_DIR} \
  && tar -xzf ${THIRDPARTY}/paho.mqtt.cpp.tar.gz \
  && cd paho.mqtt.cpp-1.2.0/ \
  && cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_BUILD_EXAMPLES=OFF \
    -DPAHO_WITH_SLL=TRUE -DPAHO_BUILD_STATIC=ON \
  && cmake --build build/ --target install

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

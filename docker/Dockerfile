FROM ubuntu:22.04

ARG BASE_DIR="/opt"
ARG TMP_DIR="/tmp"

ARG DAS_NODE_DIR="${BASE_DIR}/hyperon_das_node"
ARG DATA_DIR="${BASE_DIR}/data"
ARG PROTO_DIR="${BASE_DIR}/proto"
ARG BAZEL_DIR="${BASE_DIR}/bazel"
ARG THIRDPARTY="${BASE_DIR}/3rd-party"

ENV CPLUS_INCLUDE_PATH="/opt/3rd-party/mbedcrypto/include/"
ENV CC=/usr/bin/gcc

RUN mkdir -p ${DAS_NODE_DIR} ${DATA_DIR} \
  ${BAZEL_DIR} ${PROTO_DIR} ${THIRDPARTY}

VOLUME ${DAS_NODE_DIR}

RUN apt-get update &&\
  apt-get install -y git build-essential autoconf libtool pkg-config curl gcc g++ \
  protobuf-compiler libmbedcrypto7 python3 pip cmake make python3 pip libssl-dev unzip

RUN pip install --no-cache-dir nanobind==2.1.0

WORKDIR ${THIRDPARTY}
COPY assets/3rd-party.tgz .
RUN --mount=type=cache,target=/root/.cache/bazel \
  tar xzvf 3rd-party.tgz &&\
  rm -f 3rd-party.tgz &&\
  mkdir -p ${DAS_NODE_DIR}/src/3rd-party &&\
  ln -s ${THIRDPARTY} ${DAS_NODE_DIR}/src/3rd-party

WORKDIR ${TMP_DIR}

COPY deps/* .

RUN chmod +x bazel-7.4.1-installer-linux-x86_64.sh \
  && ./bazel-7.4.1-installer-linux-x86_64.sh

RUN tar -xzf paho.mqtt.c.tar.gz \
  && tar -xzf paho.mqtt.cpp.tar.gz

WORKDIR ${TMP_DIR}/paho.mqtt.c-1.3.9
RUN cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_WITH_SSL=OFF  -DPAHO_HIGH_PERFORMANCE=ON -DPAHO_BUILD_STATIC=ON \
  && cmake --build build/ --target install

WORKDIR ${TMP_DIR}/paho.mqtt.cpp-1.2.0
RUN cmake -Bbuild -H. -DPAHO_WITH_MQTT_C=ON -DPAHO_BUILD_EXAMPLES=OFF -DPAHO_WITH_SSL=FALSE -DPAHO_BUILD_STATIC=ON \
  && cmake --build build/ --target install

WORKDIR "${DAS_NODE_DIR}"

COPY . .

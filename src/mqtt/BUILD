package(default_visibility = ["//visibility:public"])

cc_library(
    name = "mqtt_client_lib",
    srcs = glob(["*.cc"]),
    hdrs = glob(["*.h"]),
    linkopts = [
        "-lpaho-mqtt3as",
    ],
)

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "mqtt_client_lib",
    srcs = glob(["*.cc"]),
    hdrs = glob(["*.h"]),
    includes = ["."],
    alwayslink = 1,
    linkstatic = 1,
    linkopts = [ "-L/usr/local/lib -lpaho-mqtt3as -lpaho-mqttpp3 -pthread"],
)

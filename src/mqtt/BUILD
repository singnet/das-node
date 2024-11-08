package(default_visibility = ["//visibility:public"])

# cc_import(
#   name = "paho_mqtt3as",
#   static_library = "libpaho-mqtt3as.a",
#   shared_library = "libpaho-mqtt3as.so",
#   hdrs = glob(["mqtt_hdrs/*.h"]),
# )
#
# cc_import(
#   name = "paho_mqttpp3",
#   shared_library = "libpaho-mqttpp3.so",
#   hdrs = glob(["mqtt_hdrs/*.h"]),
# )

cc_library(
    name = "mqtt_client_lib",
    srcs = glob(["*.cc"]),
    hdrs = glob(["*.h"]),
    alwayslink = 1,
    linkstatic = 0,
    linkopts = ["-lpaho-mqtt3as -lpaho-mqttpp3 -pthread"],
    # deps = [
    #   ":paho_mqtt3as",
    #   ":paho_mqttpp3",
    # ]
)

# RUN g++ client.cc -o client -Iclient.h -lpaho-mqttpp3 -lpaho-mqtt3as -pthread

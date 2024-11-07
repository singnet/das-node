package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "mqtt_client_lib",
    srcs = [ "client.cc", ],
    hdrs = [ "client.h", ],
    deps = [
        "@paho-mqttpp3//:mqttpp3",  # Add the Paho MQTT C++ client library
        "@paho-mqtt3as//:mqtt3as",  # Paho MQTT 3.1.1 C client (async library)
    ],
    # copts = [
    #     "-std=c++17",       # Set the C++ standard to C++17
    # ],
    linkopts = [
        "-pthread",          # Link pthread for multi-threading support
    ],
)

package(default_visibility = ["//visibility:public"])

cc_library(
    name = "cache_node_lib",
    srcs = glob(["*.cc"]),
    hdrs = glob(["*.h"]),
    includes = ["."],
    alwayslink = 1,
    linkstatic = 1,
    features = ["fully_static_link"],
    deps = [
        "//atom_space_node:atom_space_node_lib",
        "@com_github_singnet_das_proto//:atom_space_node_cc_grpc",
    ],
)

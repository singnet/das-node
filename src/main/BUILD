package(default_visibility = ["//visibility:public"])

cc_library(
    name = "main_lib",
    srcs = glob(["*.cc"]),
    hdrs = glob(["*.h"]),
    deps = [
        "//commons:commons_lib",
        "//atom_space_node:atom_space_node_lib",
        "@com_github_grpc_grpc//:grpc++",
        "@com_github_grpc_grpc//:grpc++_reflection",
        "@com_github_singnet_das_proto//:atom_space_node_cc_grpc",
    ],
)

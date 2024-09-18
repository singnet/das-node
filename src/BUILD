load("@rules_cc//cc:defs.bzl", "cc_library")

cc_library(
    name = "hyperon_das_node",
    # srcs = [],
    # defines = ["BAZEL_BUILD"],
    alwayslink = 1,
    deps = [
        "//atom_space_node:atom_space_node_lib",
        "//main:main_lib",
        "//commons:commons_lib",
        "@com_github_singnet_das_proto//:atom_space_node_cc_grpc",
        "@com_github_grpc_grpc//:grpc++",
        "@com_github_grpc_grpc//:grpc++_reflection",
    ],
)

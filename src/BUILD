load("@rules_cc//cc:defs.bzl", "cc_binary")

cc_binary(
    name = "hyperon_das_node",
    srcs = [],
    defines = ["BAZEL_BUILD"],
    linkstatic = 1,
    features = ["fully_static_link"],
    deps = [
        "//atom_space_node:atom_space_node_lib",
        "//main:main_lib",
        "//commons:commons_lib",
        "@com_github_singnet_das_proto//:atom_space_node_cc_grpc",
        "@com_github_grpc_grpc//:grpc++",
        "@com_github_grpc_grpc//:grpc++_reflection",
    ],
)

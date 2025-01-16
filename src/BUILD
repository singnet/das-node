load("@rules_cc//cc:defs.bzl", "cc_binary")

package(default_visibility = ["//visibility:public"])

cc_binary(
    name = "hyperon_das_node",
    srcs = [],
    defines = ["BAZEL_BUILD"],
    linkstatic = 1,
    features = ["fully_static_link"],
    deps = [
        "//distributed_algorithm_node:distributed_algorithm_node_lib",
        "//main:main_lib",
        "//commons:commons_lib",
        "@com_github_singnet_das_proto//:atom_space_node_cc_grpc",
        # "@com_github_singnet_das_proto//:distributed_algorithm_node_cc_grpc",
        "@com_github_grpc_grpc//:grpc++",
        "@com_github_grpc_grpc//:grpc++_reflection",
    ],
)

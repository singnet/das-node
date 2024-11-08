cc_test(
    name = "request_queue_test",
    srcs = ["request_queue_test.cc"],
    size = "small",
    copts = [
      "-Iexternal/gtest/googletest/include",
      "-Iexternal/gtest/googletest",
    ],
    deps = [
        "@com_github_google_googletest//:gtest_main",
        "//commons:commons_lib",
    ],
    linkstatic = 1
)

cc_test(
    name = "leadership_broker_test",
    srcs = ["leadership_broker_test.cc"],
    size = "small",
    copts = [
      "-Iexternal/gtest/googletest/include",
      "-Iexternal/gtest/googletest",
    ],
    deps = [
        "@com_github_google_googletest//:gtest_main",
        "//distributed_algorithm_node:distributed_algorithm_node_lib",
    ],
    linkstatic = 1
)

cc_test(
    name = "message_broker_test",
    srcs = ["message_broker_test.cc"],
    size = "small",
    copts = [
      "-Iexternal/gtest/googletest/include",
      "-Iexternal/gtest/googletest",
    ],
    deps = [
        "@com_github_google_googletest//:gtest_main",
        "//distributed_algorithm_node:distributed_algorithm_node_lib",
    ],
    linkstatic = 1
)

cc_test(
    name = "distributed_algorithm_node_test",
    srcs = ["distributed_algorithm_node_test.cc"],
    size = "medium",
    copts = [
      "-Iexternal/gtest/googletest/include",
      "-Iexternal/gtest/googletest",
    ],
    deps = [
        "@com_github_google_googletest//:gtest_main",
        "//distributed_algorithm_node:distributed_algorithm_node_lib",
    ],
    linkstatic = 1
)

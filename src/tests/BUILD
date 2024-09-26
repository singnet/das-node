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
        "//atom_space_node:atom_space_node_lib",
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
        "//cache_node:cache_node_lib",
        "//atom_space_node:atom_space_node_lib",
    ],
    linkstatic = 1
)

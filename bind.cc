#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>

#include "src/cache_node/CacheNode.h"

namespace nb = nanobind;
using namespace cache_node;

NB_MODULE(hyperon_das_node, m) {
  nb::class_<CacheNodeClient>(m, "CacheNodeClient")
    .def(nb::init<const string&, string&>())
    .def("node_joined_network", &CacheNodeClient::node_joined_network)
    ;

}

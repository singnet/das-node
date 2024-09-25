#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

#include "atom_space_node/AtomSpaceNode.h"
#include "cache_node/CacheNode.h"

namespace nb = nanobind;

using namespace atom_space_node;
using namespace cache_node;


NB_MODULE(hyperon_das_node_ext, m) {
  //START AtomSpaceNode Class
  nb::class_<AtomSpaceNode>(m, "AtomSpaceNode")
    .def("join_network", &AtomSpaceNode::join_network)
    .def("is_leader", &AtomSpaceNode::is_leader)
    .def("leader_id", &AtomSpaceNode::leader_id)
    .def("has_leader", &AtomSpaceNode::has_leader)
    .def("add_peer", &AtomSpaceNode::add_peer, nb::arg("peer_id"))
    .def("node_id", &AtomSpaceNode::node_id)
    //TODO: the args, argument is collections.abc.Sequence[str], is that okay?
    .def(
      "broadcast",
      &AtomSpaceNode::broadcast,
      nb::arg("command"),
      nb::arg("args"))
    //TODO: the args, argument is collections.abc.Sequence[str], is that okay?
    .def(
      "send",
      &AtomSpaceNode::send,
      nb::arg("command"),
      nb::arg("args"),
      nb::arg("recipient"))
    .def(
      "node_joined_network",
      &AtomSpaceNode::node_joined_network,
      nb::arg("node_id"))
    .def("cast_leadership_vote", &AtomSpaceNode::cast_leadership_vote);
  //END AtomSpaceNode Class

  // cache_node submodle
  nb::module_ cache_node = m.def_submodule("cache_node");
  nb::class_<CacheNode, AtomSpaceNode>(cache_node, "CacheNode")
    //TODO: is this required on the python package?
    // If so, how to propperly bind it?
    .def("message_factory", &CacheNode::message_factory);

  nb::class_<CacheNodeServer, AtomSpaceNode>(cache_node, "CacheNodeServer")
    .def(nb::init<const string&>());

  nb::class_<CacheNodeClient, CacheNode>(cache_node, "CacheNodeClient")
    .def(nb::init<const string&, string&>());
  // END cache_module
}

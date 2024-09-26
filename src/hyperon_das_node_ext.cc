#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/trampoline.h>

#include "atom_space_node/AtomSpaceNode.h"
#include "atom_space_node/Message.h"
#include "atom_space_node/MessageBroker.h"
#include "atom_space_node/LeadershipBroker.h"
#include "cache_node/CacheNode.h"

namespace nb = nanobind;
using namespace nb::literals;

using namespace std;
using namespace atom_space_node;
using namespace cache_node;

class AtomSpaceNodeTrampoline : public AtomSpaceNode {
public:
  NB_TRAMPOLINE(AtomSpaceNode, 3);
  Message *message_factory(string &command, vector<string> &args) override {
    NB_OVERRIDE(message_factory, command, args);
  };
  void node_joined_network(const string &node_id) override {
    NB_OVERRIDE_PURE(node_joined_network, node_id);
  };
  string cast_leadership_vote() override {
    NB_OVERRIDE_PURE(cast_leadership_vote);
  };
};

class AtomSpaceNodePublicist : public AtomSpaceNode {
public:
  using AtomSpaceNode::AtomSpaceNode;
  using AtomSpaceNode::message_factory;
};


NB_MODULE(hyperon_das_node_ext, m) {
  // Message.h
  nb::class_<Message>(m, "Message")
    .def("act", &Message::act);
  // end Message.h

  // LeadershipBroker.h
  nb::enum_<LeadershipBrokerType>(m, "LeadershipBrokerType")
    .value("SINGLE_MASTER_SERVER", LeadershipBrokerType::SINGLE_MASTER_SERVER);
  nb::class_<LeadershipBroker>(m, "LeadershipBroker")
    .def_static("factory", &LeadershipBroker::factory)
    .def("leader_id", &LeadershipBroker::leader_id)
    .def("set_leader_id", &LeadershipBroker::set_leader_id)
    .def("has_leader", &LeadershipBroker::has_leader)
    .def("set_message_broker", &LeadershipBroker::set_message_broker);
  // end LeadershipBroker.h

  // MessageBroker.h
  nb::enum_<MessageBrokerType>(m, "MessageBrokerType")
    .value("GRPC", MessageBrokerType::GRPC);
  nb::class_<MessageBroker>(m, "MessageBroker")
    .def_static("factory", &MessageBroker::factory)
    .def("add_peer", &MessageBroker::add_peer)
    .def("join_network", &MessageBroker::join_network)
    .def(
      "broadcast",
      &MessageBroker::broadcast,
      "command"_a,
      "args"_a)
    .def(
      "send",
      &MessageBroker::send,
      "command"_a,
      "args"_a,
      "recipient"_a);
  // end MessageBroker.h

  // AtomSpaceNode.h
  nb::class_<AtomSpaceNode, AtomSpaceNodeTrampoline>(m, "AtomSpaceNode")
    .def(nb::init<string, LeadershipBrokerType, MessageBrokerType>(), "node_id"_a, "leadership_algorithm"_a, "messaging_backend"_a)
    .def("join_network", &AtomSpaceNode::join_network)
    .def("is_leader", &AtomSpaceNode::is_leader)
    .def("leader_id", &AtomSpaceNode::leader_id)
    .def("has_leader", &AtomSpaceNode::has_leader)
    .def("add_peer", &AtomSpaceNode::add_peer, "peer_id"_a)
    .def("node_id", &AtomSpaceNode::node_id)
    .def("broadcast", &AtomSpaceNode::broadcast, "command"_a, "args"_a)
    .def("broadcast2", &AtomSpaceNode::broadcast)
    .def(
      "send",
      &AtomSpaceNode::send,
      "command"_a,
      "args"_a,
      "recipient"_a)
    .def(
      "node_joined_network",
      &AtomSpaceNode::node_joined_network,
      "node_id"_a)
    .def("cast_leadership_vote", &AtomSpaceNode::cast_leadership_vote)
    .def("message_factory", &AtomSpaceNodePublicist::message_factory);
  //end atomspacenode.h

  // cache_node submodle
  nb::module_ cache_node = m.def_submodule("cache_node");
  nb::class_<CacheNode, AtomSpaceNode>(cache_node, "CacheNode")
    .def("message_factory", &CacheNode::message_factory);

  nb::class_<CacheNodeServer, AtomSpaceNode>(cache_node, "CacheNodeServer")
    .def(nb::init<const string&>());

  nb::class_<CacheNodeClient, CacheNode>(cache_node, "CacheNodeClient")
    .def(nb::init<const string&, string&>());
  // END cache_module
}

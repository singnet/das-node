#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>
#include <nanobind/stl/shared_ptr.h>
#include <nanobind/trampoline.h>

#include "atom_space_node/AtomSpaceNode.h"
#include "atom_space_node/Message.h"
#include "atom_space_node/MessageBroker.h"
#include "atom_space_node/LeadershipBroker.h"

namespace nb = nanobind;
using namespace nb::literals;

using namespace std;
using namespace atom_space_node;

using MessagePtr = shared_ptr<Message>;
using MessageFactoryPtr = shared_ptr<MessageFactory>;

// Python trampolines
class MessageTrampoline : public Message {
  NB_TRAMPOLINE(Message, 1);
  void act(MessageFactoryPtr node) override {
    NB_OVERRIDE_PURE(act, node);
  }
};

class MessageFactoryTrampoline : public MessageFactory {
public:
  NB_TRAMPOLINE(MessageFactory, 1);
  MessagePtr message_factory(string &command, vector<string> &args) override {
    NB_OVERRIDE_PURE(message_factory, command, args);
  };
};

class AtomSpaceNodeTrampoline : public AtomSpaceNode {
public:
  NB_TRAMPOLINE(AtomSpaceNode, 3);
  MessagePtr message_factory(string &command, vector<string> &args) override {
    NB_OVERRIDE(message_factory, command, args);
  };
  void node_joined_network(const string &node_id) override {
    NB_OVERRIDE_PURE(node_joined_network, node_id);
  };
  string cast_leadership_vote() override {
    NB_OVERRIDE_PURE(cast_leadership_vote);
  };
};


NB_MODULE(hyperon_das_node_ext, m) {

  // Message.h bindings
  nb::class_<Message, MessageTrampoline>(m, "Message")
    .def(nb::init<>())
    .def("act", &Message::act);

  nb::class_<MessageFactory, MessageFactoryTrampoline>(m, "MessageFactory")
    .def("message_factory", &MessageFactory::message_factory);

  // LeadershipBroker.h bindings
  nb::enum_<LeadershipBrokerType>(m, "LeadershipBrokerType")
    .value("SINGLE_MASTER_SERVER", LeadershipBrokerType::SINGLE_MASTER_SERVER);

  nb::class_<LeadershipBroker>(m, "LeadershipBroker")
    .def_static("factory", &LeadershipBroker::factory)
    .def("leader_id", &LeadershipBroker::leader_id)
    .def("set_leader_id", &LeadershipBroker::set_leader_id)
    .def("has_leader", &LeadershipBroker::has_leader)
    .def("set_message_broker", &LeadershipBroker::set_message_broker);

  // MessageBroker.h bindings
  nb::enum_<MessageBrokerType>(m, "MessageBrokerType")
    .value("GRPC", MessageBrokerType::GRPC)
    .value("RAM", MessageBrokerType::RAM);
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

  // AtomSpaceNode.h bindings
  nb::class_<AtomSpaceNode, MessageFactory, AtomSpaceNodeTrampoline>(m, "AtomSpaceNode")
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
    .def("message_factory", &AtomSpaceNode::message_factory);
}

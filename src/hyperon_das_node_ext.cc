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
using namespace nb::literals; // Enables use of literal "_a" for named arguments

using namespace std;
using namespace atom_space_node;

// Shared pointers aliases
using MessagePtr = shared_ptr<Message>;
using MessageFactoryPtr = shared_ptr<MessageFactory>;

// **************************** Python Trampolines ****************************
// Trampolines allow Python subclasses to override C++ methods.
// For more information: https://nanobind.readthedocs.io/en/latest/classes.html#overriding-virtual-functions-in-python

class MessageTrampoline : public Message {
  // Defines a trampoline for the BaseClass
  // The count (1) denotes the total number of virtual method slots that can be
  // overriden within Python.
  NB_TRAMPOLINE(Message, 1); 
  void act(MessageFactoryPtr node) override {
    // Allows Python to override a pure virtual method
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
  // Defines a trampoline for the BaseClass
  // Since we are overriding 3 methods in Python, thon
  NB_TRAMPOLINE(AtomSpaceNode, 3);
  MessagePtr message_factory(string &command, vector<string> &args) override {
    // Allows Python to override a non pure virtual method
    NB_OVERRIDE(message_factory, command, args);
  };
  void node_joined_network(const string &node_id) override {
    NB_OVERRIDE_PURE(node_joined_network, node_id);
  };
  string cast_leadership_vote() override {
    NB_OVERRIDE_PURE(cast_leadership_vote);
  };
};
// ****************************************************************************

// Create the Python module 'hyperon_das_node_ext'
NB_MODULE(hyperon_das_node_ext, m) {

  // Message.h bindings
  nb::class_<Message, MessageTrampoline>(m, "Message")
    .def(nb::init<>())
    .def("act", &Message::act); // Bind the act method (can be overriden in Python)

  nb::class_<MessageFactory, MessageFactoryTrampoline>(m, "MessageFactory")
    .def("message_factory", &MessageFactory::message_factory); // Bind the message_factory method (can be overriden in Python)

  // LeadershipBroker.h bindings
  // Binds the enum LeadershipBrokerType and all of it's values.
  // Needs to be updated whenever a new LeadershipBrokerType is added.
  nb::enum_<LeadershipBrokerType>(m, "LeadershipBrokerType")
    .value("SINGLE_MASTER_SERVER", LeadershipBrokerType::SINGLE_MASTER_SERVER);

  // MessageBroker.h bindings
  // Binds the enum MessageBrokerType and all of it's values.
  // Needs to be updated whenever a new MessageBrokerType is added.
  nb::enum_<MessageBrokerType>(m, "MessageBrokerType")
    .value("GRPC", MessageBrokerType::GRPC)
    .value("RAM", MessageBrokerType::RAM);

  // AtomSpaceNode.h bindings
  nb::class_<AtomSpaceNode, MessageFactory, AtomSpaceNodeTrampoline>(
      m, "AtomSpaceNode")
      .def(nb::init<string, LeadershipBrokerType, MessageBrokerType>(),
           "node_id"_a, "leadership_algorithm"_a, "messaging_backend"_a)
      .def("join_network", &AtomSpaceNode::join_network)
      .def("is_leader", &AtomSpaceNode::is_leader)
      .def("leader_id", &AtomSpaceNode::leader_id)
      .def("has_leader", &AtomSpaceNode::has_leader)
      // Whenever we have a parameter that is a pointer or a reference, we need
      // to specify the name of the argument. Otherwise nanobind will add a
      // default arg0, arg1, etc.
      .def("add_peer", &AtomSpaceNode::add_peer, "peer_id"_a)
      .def("node_id", &AtomSpaceNode::node_id)
      .def("broadcast", &AtomSpaceNode::broadcast, "command"_a, "args"_a)
      .def("send", &AtomSpaceNode::send, "command"_a, "args"_a, "recipient"_a)
      .def("node_joined_network", &AtomSpaceNode::node_joined_network,
           "node_id"_a)
      .def("cast_leadership_vote", &AtomSpaceNode::cast_leadership_vote)
      .def("message_factory", &AtomSpaceNode::message_factory);
}

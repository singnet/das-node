from abc import ABC, abstractmethod

from messaging.enums import MessageFramework, MessageType
from messaging.exceptions import InvalidMessageTypeException, InvalidMessagingFramework
from messaging.messages.packet import Packet, PacketSerializer


class MessageBroker(ABC):

    node: "AtomSpaceNode"
    """
    Reference to the node this broker belongs to.
    """
    packet_serializer: PacketSerializer
    """
    Defines how we serialize and deserialize packets.
    """

    def act_from_packet(self, packet: Packet) -> None:
        """
        Callbacks an action uppon receiving a packet
        Args:
            packet: The receiving packet
        Raises:
            InvalidMessageTypeException: if packet.msg_type is invalid
        """
        match packet.msg_type:
            case MessageType.LEADERSHIP_ELECTION_START:
                self.node.leadership_broker.on_election_start(packet)
            case MessageType.LEADERSHIP_ELECTION_VOTE:
                self.node.leadership_broker.on_vote_received(packet)
            case MessageType.LEADERSHIP_ANNOUNCEMENT:
                self.node.leadership_broker.on_leader_announced(packet)
            case _:
                raise InvalidMessageTypeException

    @abstractmethod
    def start(self) -> None:
        """
        Starts the background thread that listens to new messages.
        """

    @abstractmethod
    def stop(self) -> None:
        """
        Stop the background thread that listens to new messages.
        """

    @abstractmethod
    def get_all_known_nodes(self) -> set[int]:
        """
        List of all knwn nodes in the network. Not including this node.
        """
        raise NotImplementedError

    @abstractmethod
    def broadcast(self, packet: Packet):
        """
        Broadcast a message to all nodes.

        Args:
            packet: Packet to broadcast to all nodes
        """
        raise NotImplementedError

    @abstractmethod
    def send(self, packet: Packet, dst: int):
        """
        Send a message to a specific node.
        Args:
            packet: Packet to send
            dst: Destination node id
        """
        raise NotImplementedError

    @abstractmethod
    def receive(self, packet: Packet) -> None:
        """
        Process incomming messages
        Args:
            packet: Received packet
        """
        raise NotImplementedError
    #
    # @abstractmethod
    # def check_incoming_messages(msg_type: MessageType = MessageType.ANY) -> bool:
    #     """
    #     Synchronously check for incoming messages.
    #     Args:
    #         msg_type: Message type to check for, by default check for any
    #         messages
    #     """
    #     raise NotImplementedError

    @staticmethod
    def factory(node: "AtomSpaceNode") -> "MessageBroker":
        """
        Get the framework of the message broker.

        Args:
            framework: Framework to use
            node: AtomSpaceNode reference
        """
        from messaging import brokers

        return brokers.MQTTBroker(node)

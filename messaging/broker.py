from abc import ABC, abstractmethod

from messaging.enums import MessageType
from messaging.exceptions import InvalidMessageTypeException
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

    def _act(self, packet: Packet) -> None:
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
            case MessageType.NODE_SHUTDOWN:
                self.node.shutdown()
            case _:
                raise InvalidMessageTypeException

    @abstractmethod
    def activate(self) -> None:
        """
        Activate the message broker so it will be able to send or receive messages.
        """

    @abstractmethod
    def deactivate(self) -> None:
        """
        Deactivate the message broker making it unable to send or receive messages.
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
        Broadcast a message to all nodes. Does not wait for messages to be received.

        Args:
            packet: Packet to broadcast to all nodes
        Raises:
            SendMessageException: if the message cannot be sent
        """
        raise NotImplementedError

    @abstractmethod
    def send(self, packet: Packet, dst: int):
        """
        Send a message to a specific node. Does not wait for messages to be received.

        Args:
            packet: Packet to send
            dst: Destination node id
        Raises:
            SendMessageException: if the message cannot be sent
        """
        raise NotImplementedError

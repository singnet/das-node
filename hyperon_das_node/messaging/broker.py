from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from messaging.messages.packet import Packet, PacketSerializer

if TYPE_CHECKING:
    from node import AtomSpaceNode


class MessageBroker(ABC):
    node: AtomSpaceNode
    """
    Reference to the node this broker belongs to.
    """
    packet_serializer: PacketSerializer
    """
    Defines how we serialize and deserialize packets.
    """

    def _act(self, packet: Packet) -> None:
        packet.msg_class().act(self.node, packet.data)

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
    def send(self, packet: Packet, dst: int | None):
        """
        Send a message to a specific node. Does not wait for messages to be received.

        Args:
            packet: Packet to send
            dst: Destination node id
        Raises:
            SendMessageException: if the message cannot be sent
        """
        raise NotImplementedError

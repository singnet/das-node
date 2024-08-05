from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from messaging.messages.message import BaseMessage


@dataclass(kw_only=True)
class Packet:
    """
    Serializable packet to be sent over the network.
    """

    msg_class: type[BaseMessage]
    """
    Type of the message to be sent/received.
    """
    data: Any
    """
    data to be sent/received.
    """
    sender: int
    """
    Id of the sender.
    """


class PacketSerializer(ABC):
    """
    Abstract class to serialize and deserialize packets.
    """

    @staticmethod
    @abstractmethod
    def serialize(packet: Packet) -> bytes:
        """
        Serialize a packet.
        Args:
            packet: Packet to serialize
        Returns:
            serialized packet in bytes
        """
        # TODO:
        # Raises:
        #     PacketSerializerException: if packet data is invalid
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def deserialize(data: bytes) -> Packet:
        """
        Deserialize data(bytes) into a Packet object.
        Args:
            data: bytes to deserialize
        Returns:
             Packet object
        """
        # TODO:
        # Raises:
        #     PacketSerializerException: if packet data is invalid
        raise NotImplementedError

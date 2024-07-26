from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass
from messaging.enums import MessageType


@dataclass
class Packet:
    """
    Serializable packet to be sent over the network.
    """
    msg_type: MessageType
    """
    Type of the message to be sent/received.
    """
    data: Any
    """
    data to be sent/received.
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
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def deserialize(data: bytes) -> Packet:
        """
        Deserialize a packet.
        """
        raise NotImplementedError


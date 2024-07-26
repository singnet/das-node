import pickle
import json

from messaging.messages.packet import Packet, PacketSerializer


class PickleSerializer(PacketSerializer):
    @staticmethod
    def serialize(packet: Packet) -> bytes:
        return pickle.dumps(packet)

    @staticmethod
    def deserialize(data: bytes) -> Packet:
        return pickle.loads(data)


class JsonSerializer(PacketSerializer):
    @staticmethod
    def serialize(packet: Packet) -> bytes:
        # TODO: raises an exception if not JSONSerializable
        packet_dict = {
            "msg_type": packet.msg_type, 
            "data": packet.data

        }
        return json.dumps(packet_dict).encode()

    @staticmethod
    def deserialize(data: bytes) -> Packet:
        packet_json = json.loads(data)
        return Packet(
            packet_json["msg_type"],
            packet_json["data"]
        )

import json
import pickle

from messaging.messages.packet import Packet, PacketSerializer


class PickleSerializer(PacketSerializer):
    @staticmethod
    def serialize(packet: Packet) -> bytes:
        # TODO: try/except pickle.PickleError and re raise custom exception
        return pickle.dumps(packet)

    @staticmethod
    def deserialize(data: bytes) -> Packet:
        # TODO: try/except pickle.PickleError and re raise custom exception
        return pickle.loads(data)


class JsonSerializer(PacketSerializer):
    @staticmethod
    def serialize(packet: Packet) -> bytes:
        # TODO: try/except JSONSerializable and re raise custom exception
        packet_dict = {"msg_type": packet.msg_type, "data": packet.data}
        return json.dumps(packet_dict).encode()

    @staticmethod
    def deserialize(data: bytes) -> Packet:
        # TODO: try/except JSONSerializable and re raise custom exception
        packet_json = json.loads(data)
        return Packet(
            msg_type=packet_json["msg_type"], data=packet_json["data"], sender=packet_json["sender"]
        )

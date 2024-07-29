from paho.mqtt.client import Client

from messaging.messages.packet import MessageType, Packet
from messaging.messages.serializers import PickleSerializer


def main():
    packet = Packet(msg_type=MessageType.LEADERSHIP_ELECTION_START, data=None, sender=0)
    mqtt = Client()
    mqtt.connect("mosquitto", 1883, 60)
    topic = "AtomSpace/broadcast"
    data = PickleSerializer.serialize(packet)
    mqtt.publish(topic, data)


if __name__ == "__main__":
    main()

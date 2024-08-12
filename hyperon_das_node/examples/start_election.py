from leadership.messages import StartElectionMessage
from messaging.messages.packet import Packet
from messaging.messages.serializers import PickleSerializer
from paho.mqtt.client import Client


def main():
    packet = Packet(msg_class=StartElectionMessage, data=None, sender=0)
    mqtt = Client()
    mqtt.connect("mosquitto", 1883, 60)
    topic = "AtomSpace/broadcast"
    data = PickleSerializer.serialize(packet)
    mqtt.publish(topic, data)


if __name__ == "__main__":
    main()

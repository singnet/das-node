from paho.mqtt.client import Client

from leadership.messages import StartJobMessage
from messaging.messages.packet import Packet
from messaging.messages.serializers import PickleSerializer


def main():
    packet = Packet(msg_class=StartJobMessage, data=None, sender=0)
    mqtt = Client()
    mqtt.connect("mosquitto", 1883, 60)
    topic = "AtomSpace/broadcast"
    data = PickleSerializer.serialize(packet)
    mqtt.publish(topic, data)


if __name__ == "__main__":
    main()

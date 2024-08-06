from paho.mqtt.client import Client

from leadership.messages import StartElectionMessage
from messaging.messages.packet import Packet
from messaging.messages.serializers import PickleSerializer

from examples.determinant.messages import StartDeterminantJob
from time import sleep


def main():
    # matrix = [        # Output: 0
    #     [1, 2, 3],
    #     [4, 5, 6],
    #     [7, 8, 9],
    # ]
    matrix = [          # Output: 49
        [2, 2, 1],
        [-3, 0, 4],
        [1, -1, 5],
    ]
    mqtt = Client()
    mqtt.connect("mosquitto", 1883, 60)
    # For now send message to the one who will becdome leader
    # There is an issue when broadcasting startjob, cause every node will start a new election
    # Need to implement a leader election in progress flag

    packet = Packet(
        msg_class=StartElectionMessage,
        data=None,
        sender=0
    )

    topic = "AtomSpace/broadcast"
    data = PickleSerializer.serialize(packet)
    mqtt.publish(topic, data)

    sleep(1)

    packet = Packet(
        msg_class=StartDeterminantJob,
        data=matrix,
        sender=0
    )

    topic = "AtomSpace/node_4"
    data = PickleSerializer.serialize(packet)
    mqtt.publish(topic, data)


if __name__ == "__main__":
    main()

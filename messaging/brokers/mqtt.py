import logging
from time import sleep

from paho.mqtt.client import Client

from messaging.broker import MessageBroker
# from messaging.enums import MessageType
from messaging.messages.packet import Packet
from messaging.messages.serializers import PickleSerializer
from node import AtomSpaceNode

log = logging.getLogger(__name__)


class MQTTBroker(MessageBroker):

    known_nodes: set[int]
    client: Client
    connected: bool = False
    """
    Paho MQTT client
    """

    def __init__(self, node: AtomSpaceNode):
        self.node = node
        self.packet_serializer = PickleSerializer()

        self.client = Client()

        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message

        self.known_nodes = set([1, 2, 3, 4, 5, 6])
        self.known_nodes.remove(self.node.id)

    def start(self) -> None:
        self.client.connect("mosquitto", 1883, 60)
        # Block until the connection is made.
        self.client.loop_start()
        # Wait a bit for connection to establish
        sleep(.5)

    def stop(self) -> None:
        self.client.loop_stop()
        self.client.disconnect()
        self.connected = False

    def on_connect(self, client, userdata, flags, rc) -> None:
        self.client.subscribe(f"AtomSpace/node_{self.node.id}")
        self.client.subscribe("AtomSpace/broadcast")
        self.connected = True

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print(f"{log.getEffectiveLevel()=}")
        log.debug("Subscribed to topic")

    def on_message(self, client, userdata, msg):
        packet = self.packet_serializer.deserialize(msg.payload)
        self.receive(packet)
        log.info(f"Received packet: {packet}")

    def receive(self, packet: Packet) -> None:
        self.act_from_packet(packet)

    def get_all_known_nodes(self) -> set[int]:
        # As of the scope of this task, the network is all set up, we don't
        # need to discover new nodes
        return self.known_nodes

    def broadcast(self, packet: Packet) -> None:
        topic = "AtomSpace/broadcast"
        msg = self.packet_serializer.serialize(packet)
        self.client.publish(topic, msg)

    def send(self, packet: Packet, dst: int) -> None:
        topic = f"AtomSpace/node_{dst}"
        msg = self.packet_serializer.serialize(packet)
        self.client.publish(topic, msg)

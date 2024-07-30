import logging
from time import sleep

from paho.mqtt.client import Client

from messaging.broker import MessageBroker
from messaging.messages.packet import Packet
from messaging.messages.serializers import PickleSerializer
from node import AtomSpaceNode

log = logging.getLogger(__name__)


class MQTTBroker(MessageBroker):
    _known_nodes: set[int]
    """
    List of known nnodes in the network
    """
    _client: Client
    """
    Paho MQTT client
    """
    _connected: bool = False
    """
    Paho MQTT client
    """

    def __init__(self, node: AtomSpaceNode):
        self.node = node
        self.packet_serializer = PickleSerializer()

        self._client = Client()

        self._client.on_connect = self._on_connect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_message = self._on_message

        self._known_nodes = set([1, 2, 3, 4, 5, 6])
        self._known_nodes.remove(self.node.id)

    # Base class methods
    def activate(self) -> None:
        self._client.connect("mosquitto", 1883, 60)
        # Block until the connection is made.
        self._client.loop_start()
        # Wait a bit for connection to establish
        sleep(0.5)

    def deactivate(self) -> None:
        self._client.loop_stop()
        self._client.disconnect()
        self._connected = False

    def get_all_known_nodes(self) -> set[int]:
        # As of the scope of this task, the network is all set up, we don't
        # need to discover new nodes
        return self._known_nodes

    def broadcast(self, packet: Packet) -> None:
        self._publish(self._broadcast_topic(), packet)

    def send(self, packet: Packet, dst: int) -> None:
        self._publish(self._node_topic(dst), packet)

    # Private methods
    def _on_connect(self, client, userdata, flags, rc) -> None:
        """
        Called when connected to MQTT broker.
        """
        self._client.subscribe(self._node_topic(self.node.id))
        self._client.subscribe(self._broadcast_topic())
        self._connected = True

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        """
        Called when subscribed to a topic.
        """
        log.debug("Subscribed to topic")

    def _on_message(self, client, userdata, msg):
        """
        Called when receiving a message.
        """
        packet = self.packet_serializer.deserialize(msg.payload)
        log.info("Received packet: %s on topic: %s", packet, msg.topic)

        if msg.topic == self._broadcast_topic() and packet.sender == self.node.id:
            # ignore broadcst messages from self
            return

        self._act(packet)

    def _publish(self, topic: str, packet: Packet) -> None:
        """
        Serialize a packet and publishes it to a topic.
        Args:
            topic: Topic to publish to
            packet: Packet to be published
        """
        msg = self.packet_serializer.serialize(packet)
        self._client.publish(topic, msg)

    def _broadcast_topic(self) -> str:
        return "AtomSpace/broadcast"

    def _node_topic(self, node_id: int) -> str:
        return f"AtomSpace/node_{node_id}"

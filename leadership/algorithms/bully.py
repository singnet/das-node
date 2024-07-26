import logging

from leadership.broker import LeadershipBroker
from messaging.messages.packet import Packet
from messaging.enums import MessageType

log = logging.getLogger(__name__)

class Bully(LeadershipBroker):

    votes: set[int]

    def __init__(self, node: "AtomSpaceNode"):
        self.node = node
        self.votes = set()

    def elect_leader(self) -> None:

        self.reset_leader()

        packet = Packet(
            msg_type=MessageType.LEADERSHIP_ELECTION_START,
            data = None
        )

        self.node.message_broker.broadcast(packet)

    def vote(self) -> None:
        packet = Packet(
            msg_type=MessageType.LEADERSHIP_ELECTION_VOTE,
            data = self.node.id
        )

        self.node.message_broker.broadcast(packet)

    def announce_leader(self) -> None:
        self._leader_id = self.node.id
        packet = Packet(
            msg_type=MessageType.LEADERSHIP_ANNOUNCEMENT,
            data = self.node.id
        )

        self.node.message_broker.broadcast(packet)

    def on_election_start(self, packet: Packet) -> None:
        self.vote()

    def on_vote_received(self, packet: Packet) -> None:
        assert isinstance(packet.data, int)
        self.votes.add(packet.data)
        self.process_votes()

    def process_votes(self):
        known_nodes = self.node.message_broker.get_all_known_nodes()
        log.debug(f"{len(known_nodes)=}")
        if not len(self.votes) == len(known_nodes) + 1:
            return
        
        if max(self.votes) == self.node.id:
            self.announce_leader()

    def on_leader_announced(self, packet: Packet) -> None:
        self._leader_id = packet.data

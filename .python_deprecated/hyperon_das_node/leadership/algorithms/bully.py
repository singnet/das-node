import logging
from typing import Any

from leadership.broker import LeadershipBroker
from leadership.messages import (
    ElectionVoteMessage,
    LeadershipAnnouncementMessage,
    StartElectionMessage,
)
from messaging.messages.packet import Packet
from node import AtomSpaceNode

log = logging.getLogger(__name__)


class Bully(LeadershipBroker):
    votes: set[int]

    def __init__(self, node: AtomSpaceNode):
        self.node = node
        self.votes = set()

        self._election_in_progress = False
        self._leader_id = None

    def elect_leader(self) -> None:
        log.debug("Starting a new leader election")
        self._reset_leader()

        packet = Packet(
            msg_class=StartElectionMessage,
            data=None,
            sender=self.node.id,
        )

        self.node.message_broker.broadcast(packet)
        self.on_election_start()

    def vote(self) -> None:
        log.debug("Casting a vote")
        packet = Packet(
            msg_class=ElectionVoteMessage,
            data=self.node.id,
            sender=self.node.id,
        )
        self.votes.add(self.node.id)
        self.node.message_broker.broadcast(packet)

    def announce_leader(self) -> None:
        log.debug("Announcing self as the new Leader")
        packet = Packet(
            msg_class=LeadershipAnnouncementMessage,
            data=self.node.id,
            sender=self.node.id,
        )
        self.node.message_broker.broadcast(packet)
        self.on_leader_announced(self.node.id)

    def on_election_start(self) -> None:
        # Ignore multile election_start messages
        if self._election_in_progress:
            return

        self._election_in_progress = True
        self.votes.clear()
        self.vote()

    def on_vote_received(self, data: int) -> None:
        self.votes.add(data)
        self.process_votes()

    def process_votes(self):
        log.debug("Processing votes")
        known_nodes = self.node.message_broker.get_all_known_nodes()
        log.debug(f"{len(known_nodes)=} == {len(self.votes)}")
        if not len(self.votes) == len(known_nodes) + 1:
            log.debug("Not enough votes to complete election")
            return

        if max(self.votes) == self.node.id:
            self.announce_leader()

    def on_leader_announced(self, data: Any) -> None:
        data = int(data)
        self._leader_id = data
        self._election_in_progress = False

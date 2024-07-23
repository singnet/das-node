from dataclasses import dataclass

from leader_election.algorithms.interface import AlgorithmInterface
from messaging.messages.leader_election import (
    ElectionStartMessage,
    ElectionVoteMessage,
    LeaderAnnouncementMessage,
)
from messaging.mqtt import Topics, mqtt


@dataclass(kw_only=True)
class Bully(AlgorithmInterface):

    def __post_init__(self):
        mqtt.subscribe(Topics.election_start, self.on_election_start)
        mqtt.subscribe(Topics.election_vote, self.vote_received)
        mqtt.subscribe(Topics.leader_announcement, self.leader_announced)

    def vote(self) -> None:
        """ """
        message = ElectionVoteMessage(
            sender=self.state.id, payload={"score": self.score}
        )
        mqtt.publish(message)

    def vote_received(self, message: ElectionVoteMessage) -> None:
        if self.state.id == message.sender:
            # Do not record own votes
            return

        # register vote
        self.votes.add(message.score)

        if len(self.votes) == len(self.state.nodes_ids) - 1:
            self.announce_leadership()

    def start_election(self) -> None:
        mqtt.publish(ElectionStartMessage(sender=self.state.id, payload={}))

    def on_election_start(self, _: ElectionStartMessage) -> None:
        self.state.reset_leader()
        self.vote()

    def leader_announced(self, message: LeaderAnnouncementMessage) -> None:
        self.state.set_leader(message.leader_id)
        self.votes.clear()

    def announce_leadership(self) -> None:
        if self.score > max(self.votes):
            message = LeaderAnnouncementMessage(sender=self.state.id, payload={})
            mqtt.publish(message)

    @property
    def score(self):
        """
        Determine the score of the node, this will be used to elect a node
        leader. The node with a higher score wins the election.
        """
        return self.state.id

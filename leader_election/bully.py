from typing import Optional
from messaging.mqtt import mqtt, Topics
from messaging.messages.leader_election import (
    ElectionStartMessage,
    ElectionVoteMessage,
    LeaderAnnouncementMessage,
)


class Bully:
    votes: list
    leader_id: Optional[int]
    is_leader: bool
    nodes: list

    def __init__(self, node_id, nodes):
        self.node_id = node_id
        self.nodes = nodes
        self.reset_leader()
        mqtt.subscribe(Topics.election_start, self.vote)
        mqtt.subscribe(Topics.election_vote, self.vote_received)
        mqtt.subscribe(Topics.leader_announcement, self.leader_announced)

    def reset_leader(self) -> None:
        self.votes = []
        self.leader_id = None
        self.is_leader = False

    def vote(self, msg: ElectionStartMessage) -> None:
        """ """
        self.reset_leader()
        message = ElectionVoteMessage(
            sender=self.node_id, payload={"score": self.score}
        )
        mqtt.publish(message)

    def vote_received(self, message: ElectionVoteMessage) -> None:
        self.votes.append(message.payload["score"])
        if len(self.votes) == len(self.nodes) - 1:
            self.announce_leadership()

    def start_election(self) -> None:
        mqtt.publish(ElectionStartMessage(sender=self.node_id, payload={}))

    def leader_announced(self, message: LeaderAnnouncementMessage) -> None:
        self.leader_id = message.sender
        self.is_leader = False
        self.votes = []

    def announce_leadership(self) -> None:
        if self.score > max(self.votes):
            message = LeaderAnnouncementMessage(sender=self.node_id, payload={})
            mqtt.publish(message)
            self.is_leader = True

    @property
    def score(self):
        """
        Determine the score of the node, this will be used to elect a node
        leader. The node with a higher score wins the election.
        """
        return self.node_id

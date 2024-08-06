""" """

from abc import ABC, abstractmethod
from typing import Any
from time import sleep

from messaging.messages import BaseMessage
from node import AtomSpaceNode

from logging import getLogger
log = getLogger(__name__)


class JobStartMessage(BaseMessage, ABC):
    """
    Abstract JobStartMessage, should be extended by all jobs.
    Use it to start the job.
    It will automatically elect a leader, if there isn't one yet.
    """

    def act(self, node: AtomSpaceNode, data: Any) -> None:
        # log.debug("Starting Job, has_leader: %s", node.leadership_broker.has_leader)
        # if not node.leadership_broker.has_leader:
        #     log.debug("starting leader election")
        #     node.leadership_broker.elect_leader()

        # log.debug("waiting for leader")
        # self.wait_leader_election(node)
        # log.debug("Leader announced Doing JOB")
        self.do_job(node, data)

    # Messages cannot have blocking calls
    def wait_leader_election(self, node: AtomSpaceNode) -> None:
        while not node.leadership_broker.has_leader:
            sleep(1)

    @abstractmethod
    def do_job(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError


class JobCompleteMessage(BaseMessage, ABC):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError


class JobFailureMessage(BaseMessage, ABC):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError


class JobStatusMessage(BaseMessage, ABC):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError


class JobStatusReplyMessage(BaseMessage, ABC):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError


class JobCancelMessage(BaseMessage, ABC):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError


class JobMessage(BaseMessage, ABC):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        raise NotImplementedError

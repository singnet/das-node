from abc import ABC, abstractmethod
from logging import getLogger
from typing import Any

from messaging.messages import BaseMessage
from node import AtomSpaceNode

log = getLogger(__name__)


class JobStartMessage(BaseMessage, ABC):
    """
    Abstract JobStartMessage, should be extended by all jobs.
    Use it to start the job.
    It will automatically elect a leader, if there isn't one yet.
    """

    def act(self, node: AtomSpaceNode, data: Any) -> None:
        if hasattr(node, "_job_requestor"):
            node.start_job()

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

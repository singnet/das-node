from logging import getLogger
from typing import Any

from messaging.messages import BaseMessage
from node import AtomSpaceNode

log = getLogger(__name__)


class JobStartMessage(BaseMessage):
    """
    Abstract JobStartMessage, should be extended by all jobs.
    Use it to start the job.
    It will automatically elect a leader, if there isn't one yet.
    """

    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.start_job(data)


class JobCompleteMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.job_completed(data)


class JobFailureMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.job_failed(data)


class JobStatusMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.job_status(data)


class JobStatusReplyMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        log.info("A JobStatus was received on node_id: %s with data %s", node.id, data)


class JobCancelMessage(BaseMessage):
    def act(self, node: AtomSpaceNode, data: Any) -> None:
        node.job_cancelled(data)

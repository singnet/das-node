from logging import getLogger
from time import sleep
from typing import Any

from job_management import messages as job_messages
from messaging.messages.packet import Packet

from .determinant_node import DeterminantNode

log = getLogger(__name__)


class StartDeterminantJob(job_messages.JobStartMessage):
    def do_job(self, node: DeterminantNode, data: Any) -> None:
        log.debug("Doing DeterminantJob")
        # stores the matrix in the node state
        node.matrix = data

        if not node.leadership_broker.is_leader:
            return

        log.debug("Node is leader, sending Determinant2Job")
        self.request_determinant_2x2(node)
        log.debug("Awaiting results")

    def request_determinant_2x2(self, node: DeterminantNode) -> None:
        # list of known_nodes to send a request to calculate the 2x2 determinant
        peers = list(node.message_broker.get_all_known_nodes())

        # safe check, We assume this condition is satisfied
        assert len(peers) >= len(node.matrix)

        for i in range(len(node.matrix)):
            cofactor = (-1) ** i * node.matrix[0][i]
            packet = Packet(
                msg_class=Determinant2Message, data=(node.matrix, i, cofactor), sender=node.id
            )
            node.message_broker.send(packet=packet, dst=peers[i])

    def job_complete(self, node: DeterminantNode) -> None:
        assert None not in node.results_2x2  # safe check
        result = sum(a for a in node.results_2x2 if a is not None)

        log.info(f"Result: {result}")
        # Send back JobComplete

    def wait_results(self, node: DeterminantNode) -> None:
        while any(result is None for result in node.results_2x2):
            sleep(1)


class Determinant2Message(job_messages.JobMessage):
    def act(self, node: DeterminantNode, data: Any) -> None:
        matrix, index, cofactor = data
        node.matrix = matrix
        submatrix = self.get_submatrix(node.matrix, 0, index)
        determinant = submatrix[0][0] * submatrix[1][1] - submatrix[0][1] * submatrix[1][0]
        # Send result back to leader
        packet = Packet(
            msg_class=Determinant2ReplyMessage,
            data=(index, cofactor, determinant),
            sender=node.id,
        )
        node.message_broker.send(packet, node.leadership_broker.leader_id)

    def get_submatrix(self, matrix, row, col):
        return [row[:col] + row[col + 1 :] for row in (matrix[:row] + matrix[row + 1 :])]


class Determinant2ReplyMessage(job_messages.JobMessage):
    """
    Received by the leader to store results in the node state.
    """

    def act(self, node: DeterminantNode, data: Any) -> None:
        log.info(data)
        index, cofactor, determinant = data
        # Stores result
        node.results_2x2[index] = cofactor * determinant
        if all(r is not None for r in node.results_2x2):
            log.info("All results arrived")
            determinant = sum(r for r in node.results_2x2)
            log.info("Determinant ouput: %s", determinant)

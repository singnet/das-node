import json
from enum import StrEnum
from dataclasses import dataclass, field
from datetime import datetime


class Topics(StrEnum):
    # Election Topics
    election_start = "election/start"
    election_vote = "election/vote"
    leader_announcement = "election/leader_announcement"
    # Job Management Topics
    job_request = "job/request"
    job_status = "job/status"
    job_result = "job/result"
    # Telemetry Topics
    telemetry_heartbeat = "telemetry/heartbeat"
    telemetry_log = "telemetry/log"

    # None, should not be used
    none = "none"


@dataclass(kw_only=True)
class Message:
    """Base message structure"""

    sender: int
    payload: dict
    sequence_number: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    topic: Topics = Topics.none

    @property
    def json(self) -> str:
        """
        Returns the message as a json serialized string
        Example: {
            "header": {
                "senderId": 1,
                "sequenceNumber": 12345,
                "timestamp": "2024-01-01T00:00:00Z",
                "messageType": "election/vote" // "telemetry/heartbeat"
            },
            "payload": {
                "term": 1,
                "candidateId": 2,
                "lastLogIndex": 3,
                "lastLogTerm": 4
            },
        }


        """
        data = {
            "header": {
                "senderId": self.sender,
                "sequenceNumber": self.sequence_number,
                "timestamp": self.timestamp.isoformat(),
                "messageType": self.topic,
            },
            "payload": self.payload,
        }

        return json.dumps(data)

    @staticmethod
    def from_json(str_data: str) -> "Message":
        """
        Parses a json string and returns a Message object
        """
        data: dict = json.loads(str_data)
        sender = int(data["header"]["senderId"])
        payload = data["payload"]
        topic = Topics(data["header"]["messageType"])
        sequence_number = int(data["header"]["sequenceNumber"])
        timestamp = datetime.fromisoformat(data["header"]["timestamp"])

        return Message(
            sender=sender,
            payload=payload,
            topic=topic,
            sequence_number=sequence_number,
            timestamp=timestamp,
        )

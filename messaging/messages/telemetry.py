from dataclasses import dataclass
from messaging.messages.base import Message, Topics


@dataclass(kw_only=True)
class HeartbeatMessage(Message):
    """ """

    topic = Topics.telemetry_heartbeat


@dataclass(kw_only=True)
class TelemetryLogMessage(Message):
    """ """

    topic: Topics = Topics.telemetry_log

from itertools import count
from logging import getLogger
from typing import Callable

from paho.mqtt.client import Client

from messaging.messages import job_management, leader_election, telemetry
from messaging.messages.base import Message, Topics

log = getLogger(__name__)


# TODO: build an Client class on the messaging module, that instances this
# class, the Client class should be a singleton and only reference the protocol
# (MQTT, gRPC, etc) on that class, so it is transparent for the other modules


# TODO: Try to inherit from Client class, less boilerplate code
class MQTTSingleton:
    """
    Singleton class that handles all the MQTT communication.
    """

    _instance = None
    _sequence = count(1)  # starts at 1

    def __new__(cls, *args, **kwargs):
        """
        Singleton implementation
        """
        if not cls._instance:
            cls._instance = super(MQTTSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.setup_client()
        return cls._instance

    def setup_client(self):
        """ """
        # TODO: change it all to a config/enf file
        self.host = "localhost"
        self.port = 1883
        self.timeout = 60
        self.client = Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.connect(self.host, self.port, self.timeout)
        self.client.loop_start()  # background thread

    def on_connect(self, client, userdata, flags, rc) -> None:
        """
        After connection successfull, subscribe to all topics
        """
        qos = 1
        self.client.subscribe(
            [(topic, qos) for topic in Topics if topic != Topics.none]
        )

    def on_subscribe(self, client, userdata, mid, granted_qos) -> None:
        """ """
        log.info("Subscribed")

    def on_message(self, client, userdata, msg) -> None:
        """
        Receives all messages from the broker
        parses them into a Message object
        and calls the callback function, based on the topic
        """
        message = Message.from_json(msg.payload)
        callback_name = self.topic_to_callback_name(message.topic)
        if hasattr(self, callback_name):
            callback = getattr(self, callback_name)
            return callback(message)

        log.warning(
            "message received % but callback was not set, message: %s",
            callback_name,
            message,
        )

    def publish(self, message: Message):
        """ """
        # TODO: consider using a thread lock to avoid race conditions
        message.sequence_number = next(MQTTSingleton._sequence)
        self.client.publish(message.topic, message.json)

    def subscribe(self, topic: str, callback: Callable[[Message], None]):
        """ """
        callback_name = self.topic_to_callback_name(topic)
        log.warning("subscribing to %s", callback_name)
        setattr(self, callback_name, callback)

    def topic_to_callback_name(self, topic: str) -> str:
        """ """
        return f"on_{topic.replace('/', '_')}"

    @classmethod
    def disconnect(cls):
        """ """
        if instance := cls._instance:
            instance.client.loop_stop()
            instance.client.disconnect()

    # def start_election(self, message: Message):
    #     self.publish(message)
    #
    # Messaging Interface:
    # Election Interface
    # def on_election_start(self, message: Message) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_election_start but callback was not set, message: %s",
    #         message,
    #     )
    #
    # def election_vote(self, message: leader_election.ElectionVoteMessage) -> None:
    #     self.publish(message)
    #
    # def on_election_vote(self, message: leader_election.ElectionVoteMessage) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_election_vote but callback was not set, message: %s",
    #         message,
    # )
    #
    # def election_leader_announcement(
    #     self, message: leader_election.LeaderAnnouncementMessage
    # ) -> None:
    #     self.publish(message)
    #
    # def on_election_leader_announcement(
    #     self, message: leader_election.LeaderAnnouncementMessage
    # ) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_election_leader_announcement but callback was not set, message: %s",
    #         message,
    #     )
    #
    # # Job Management Interface
    # def on_job_request(self, message: job_management.JobRequestMessage) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_job_request but callback was not set, message: %s",
    #         message,
    #     )
    #
    # def on_job_status(self, message: job_management.JobStatusMessage) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_job_status but callback was not set, message: %s",
    #         message,
    #     )
    #
    # def on_job_result(self, message: job_management.JobResultMessage) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_job_result but callback was not set, message: %s",
    #         message,
    #     )
    #
    # # Telemetry Interface
    # def on_telemetry_heartbeat(self, message: telemetry.TelemetryLogMessage) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_telemetry_heartbeat but callback was not set, message: %s",
    #         message,
    #     )
    #
    # def on_telemetry_log(self, message: telemetry.TelemetryLogMessage) -> None:
    #     # this should be overriden by user, for now just log it as an warning
    #     log.warning(
    #         "message received on_telemetry_log but callback was not set, message: %s",
    #         message,
    #     )


mqtt = MQTTSingleton()

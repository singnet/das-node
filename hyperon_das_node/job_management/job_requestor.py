"""
A JobRequestor is a module that can request a job. It will have inside
information about the AtomSpaceNode network, like what protocol we are
currently using, also it has to know the IP of at least one node on the
Network.

This is an example of a job requestor that uses the MQTT protocol to start a
job.
"""

from job_management.messages import JobCompleteMessage, JobStartMessage
from messaging.messages import Packet, PickleSerializer
from paho.mqtt.client import Client


class JobRequestor:
    def __init__(self) -> None:
        self.mqtt = Client()
        self.mqtt.connect("mosquitto", 1883, 60)
        self.mqtt.on_message = self.on_message
        self.mqtt.subscribe("AtomSpace/broadcast", 0)
        self.mqtt.loop_start()

    def start_job(self):
        job_data = None
        packet = Packet(msg_class=JobStartMessage, data=job_data, sender=0)

        # For this example, we can broadcast the message, only the leader will
        # actually process it
        topic = "AtomSpace/broadcast"
        msg = PickleSerializer.serialize(packet)
        self.mqtt.publish(topic, msg)
        print("Message seng, waiting for JobCompleteMessage")

    def on_message(self, _client, _userdata, msg) -> None:
        packet = PickleSerializer.deserialize(msg.payload)
        if packet.msg_class == JobCompleteMessage:
            self.on_job_complete(packet)

    def on_job_complete(self, packet: Packet):
        print(packet.data)
        self.mqtt.loop_stop()


def main():
    job_requestor = JobRequestor()
    job_requestor.start_job()


if __name__ == "__main__":
    main()

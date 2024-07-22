from messaging.messages.base import Message

class JobRequestMessage(Message):
    """
    """
    topic = "job/request"


class JobStatusMessage(Message):
    """
    """
    topic = "job/status"


class JobResultMessage(Message):
    """
    """
    topic = "job/result"

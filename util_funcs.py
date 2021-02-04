import random
import string


def get_peer_id():
    rand_num = ''
    for i in range(0, 20):
        rand_num = rand_num + (random.choice(string.ascii_lowercase + string.digits))
    return rand_num


def get_transaction_id():
    return random.randint(0, 1 << 32 - 1)


class TrackerException(Exception):
    """Base class for all Tracker Exceptions"""

    mode = 'tracker'

    def __init__(self, message, data):
        self.message = message
        self.data = data

    def __repr__(self):
        return "<%s=>%s>%s:%s" % (self.__class__.__name__, self.mode, self.message, str(self.data))


class TrackerRequestException(TrackerException):
    """Exception that occurs on tracker request"""
    mode = "request"


class TrackerResponseException(TrackerException):
    """Exception that occurs on tracker response"""
    mode = "response"
print(get_transaction_id())
print(get_transaction_id())
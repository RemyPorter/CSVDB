from ..message_types import ALL_TYPES
from ..messaging.message import Message

class CommitLog:
    def __init__(self, path, bus):
        self.handle = open(path, "a")
        self.bus = bus
        bus.subscribe_all(self)

    def __call__(self, message):
        try:
            self.handle.write(str(message) + "\n")
            self.handle.flush()
        except e:
            m = Message("system_emergency", error=e)
from .datamodel.bucketiface import BucketInterface
from .messaging.bus import InternalBus
from .messaging.message import Message
from .storage.commitlog import CommitLog

class Database:
    def __init__(self):
        self.bus = InternalBus()
        self.buckets = BucketInterface(self.bus)
        self.commitlog = CommitLog("log.txt", self.bus)
        self.bus.subscribe("system_emergency", self)
        #TODO: add bootstrapping, and, y'know, database functionaliy

    def __call__(self, message):
        if message.operation == "system_emergency":
            print("Cannot continue.")
            print(message["error"])
            import sys
            sys.exit(-1)
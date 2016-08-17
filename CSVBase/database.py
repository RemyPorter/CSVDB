from .datamodel.bucketiface import BucketInterface
from .messaging.bus import InternalBus
from .messaging.message import Message

class Database:
    def __init__(self):
        self.bus = InternalBus()
        self.buckets = BucketInterface(self.bus)
        #TODO: add bootstrapping, and, y'know, database functionaliy
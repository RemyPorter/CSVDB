from .bucket import Bucket
from .bucketmessenger import bucket_message
class DuplicateBucketError(Exception):
    pass

class BucketInterface:
    """
    Wrap the set of active buckets and support messages
    for accessing those buckets.

    >>> from ..messaging.bus import InternalBus
    >>> from ..messaging.message import Message
    >>> bus = InternalBus()
    >>> bi = BucketInterface(bus)
    >>> m = Message("system_create_bucket", name="foo")
    >>> m["name"]
    'foo'
    >>> bus.publish(None, m)
    >>> bi.buckets["foo"].name
    'foo'
    """
    def __init__(self, bus):
        self.buckets = dict()
        bus.subscribe("system_create_bucket",
            getattr(self, "_create_message"))
        bus.subscribe("system_drop_bucket",
            getattr(self, "_drop_message"))
        self._bus = bus

    def create_bucket(self, name):
        if name in self.buckets.keys():
            raise DuplicateBucketError("Bucket already exists.")
        self.buckets[name] = bucket_message(Bucket(name), self._bus)

    def drop_bucket(self, name):
        del self.buckets[name]

    def _create_message(self, message):
        self.create_bucket(message["bucket"])

    def _drop_message(self, message):
        self.drop_bucket(message["bucket"])

if __name__ == '__main__':
    import doctest
    doctest.testmod()
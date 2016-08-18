from ..datamodel.bucketmessenger import bucket_message
from ..messaging.message import build_message
import time

class OpCounter:
    """
    Simple counter to track the number of operations performed
    on a bucket. This is specifically for DML operations, and
    based on configuration (num ops, refractory period, time)
    it will trigger a flush.

    >>> oc = OpCounter(TestBucket(), TestBus(), 2, 0)
    >>> oc.create()
    >>> oc.create()
    >>> oc.create()
    Test_flush:{}
    """
    def __init__(self, bucket, bus, threshold, refractory=1000):
        self.bucket = bucket
        self.name = bucket.name
        bucket_message(self, bus)
        self.op_count = 0
        self.threshold = threshold
        self.refraction = refractory
        self.last_flush = time.time()
        self.bus = bus
        self.retries = 0

    def __should_flush(self):
        return self.op_count > self.threshold and \
            time.time() > self.last_flush + self.refraction

    def __handle(self):
        self.op_count += 1
        if self.__should_flush():
            m = build_message(self.bucket.name, "flush", dict())
            self.bus.publish(self, m)

    def notify(self, message, result):
        self.last_flush = time.time()
        self.op_count = 0

    def fail(self, message, exception):
        self.retries += 1
        self.__handle()

    def create(self, *args):
        self.__handle()
    def update(self, *args):
        self.__handle()
    def delete(self, *args):
        self.__handle()

if __name__ == '__main__':
    class TestBus:
        def __init__(self):
            pass
        def publish(self, sender, message):
            print(message)
        def subscribe(self, operation, subscriber):
            pass
    class TestBucket:
        def __init__(self):
            self.name = "Test"
    import doctest
    doctest.testmod()
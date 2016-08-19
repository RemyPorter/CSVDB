from ..datamodel.bucketmessenger import bucket_message
from ..messaging.message import build_message
from ..datamodel.structures.utility import format_op
import os.path
from uuid import
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

class BucketWriter:
    """
    Actually write the contents of a bucket.

    >>> bw = BucketWriter(TestBucket())
    >>> from io import StringIO
    >>> f = StringIO()
    >>> bw._write(f)
    >>> print(f)
    1, 2, 3, 4
    <BLANKLINE>
    """
    def __init__(self, bucket):
        self.bucket = bucket

    def write(self):
        try:
            fname = "{0}.{1}.dat".format(self.bucket.name, uuid.uuid1())
            path = fname #os.path.join(self.datadir, fname)
            with open(path, "a") as f:
                self._write(f)
        except Exception as e:
            self.bus.big_red_button(self, e)
            raise e

    def _write(self, f):
        for row in self.bucket.search():
            first = True
            for col in row:
                if not first:
                    f.write(",")
                first = False
                f.write(col)
                f.write("\n")
                f.flush()


class BucketFlusher:
    """
    Flushes the in-memory contents of a bucket to a file.

    >>> bf = BucketFlusher(TestBucket(), TestBus())
    >>> bf(None)
    flush_complete:{}
    """
    def __init__(self, bucket, bus):
        self.bucket = bucket
        self.bus = bus
        bus.subscribe(format_op(bucket.name, "flush"), self)
        self.writer = BucketWriter(bucket)

    def __call__(self, message):
        try:
            self.writer.write()
            self.bucket.reset()
            m = build_message(self.bucket.name, "flush_complete", dict())
            self.bus.publish(m)
        except:
            pass #we can safely swallow this because any exceptions
                # got passed up with a big_red_button

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
        def search(self, *args):
            return [
                [1, 2, 3, 4]
            ]
        def reset(self):
            print("Reset")
    import doctest
    doctest.testmod()
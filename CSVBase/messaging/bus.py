from concurrent.futures import *
from collections import defaultdict
from .message import Message
class InternalBus:
    """
    A simple, asynchronous message bus for passing messages through the application.
    >>> b = InternalBus()
    >>> ds0 = __DummySubscriber(b)
    >>> ds1 = __DummySubscriber(b)
    >>> dp = __DummyPublisher()
    >>> dp.send(b)
    dummy
    dummy
    Success!
    Success!
    """
    def __init__(self):
        self.subscriptions = defaultdict(set)
        self.__executor = ThreadPoolExecutor()

    def publish(self, sender, message, timeout=10):
        fs = [self.__executor.submit(s, message) for s in self.subscriptions[message.operation]]
        for f in as_completed(fs, timeout):
            if f.exception() and hasattr(sender, "fail"):
                sender.fail(f.exception())
            elif hasattr(sender, "notify"):
                sender.notify(f.result())

    def subscribe(self, operation, subscriber):
        self.subscriptions[operation].add(subscriber)

    def unsubscribe(self, subscriber):
        for k,v in self.subscriptions.items():
            v.remove(subscriber);

class __DummySubscriber:
    def __init__(self, bus):
        bus.subscribe("dummy", self)

    def __call__(self, message):
        print(message["value"])
        return True

class __DummyPublisher:
    def __init__(self):
        pass

    def send(self, bus):
        bus.publish(self, Message("dummy", value="dummy"))

    def notify(self, result):
        if result == True:
            print("Success!")

if __name__ == '__main__':
    import doctest
    doctest.testmod()
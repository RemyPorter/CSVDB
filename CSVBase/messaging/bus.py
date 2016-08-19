from concurrent.futures import *
from threading import Thread
import time
from collections import defaultdict
from .message import Message, build_message
class InternalBus:
    """
    A simple, asynchronous message bus for passing messages through the application.
    >>> b = InternalBus()
    >>> ds0 = __DummySubscriber(b)
    >>> ds1 = __DummySubscriber(b)
    >>> as0 = __AlwaysSubscriber(b)
    >>> dp = __DummyPublisher()
    >>> dp.send(b)
    Got always
    dummy
    dummy
    Success!
    Success!
    Success!
    """
    def __init__(self):
        self.subscriptions = defaultdict(set)
        self.always = set()
        self.__executor = ThreadPoolExecutor()
        self.clock = Clock(self)

    def publish(self, sender, message, timeout=10):
        all_subscriptions = self.subscriptions[message.operation] | \
            self.always
        fs = [self.__executor.submit(s, message) for s in all_subscriptions]
        for f in as_completed(fs, timeout):
            if f.exception() and hasattr(sender, "fail"):
                sender.fail(message, f.exception())
            elif hasattr(sender, "notify"):
                sender.notify(message, f.result())

    def big_red_button(self, sender, error):
        m = Message("system_emergency", source=sender, error=error)
        self.publish(sender, message)

    def subscribe(self, operation, subscriber):
        self.subscriptions[operation].add(subscriber)

    def unsubscribe(self, subscriber):
        for k,v in self.subscriptions.items():
            v.remove(subscriber)

    def subscribe_all(self, subscriber):
        self.always.add(subscriber)

class Clock:
    def __init__(self, bus):
        self.bus = bus
        self.ticks = time.time()
        self.thread = Thread(group=None, target=self, name="clock",
            daemon=True)
        self.thread.start()

    def __call__(self):
        while(True):
            curTime = time.time()
            diff = curTime - self.ticks
            self.ticks = curTime
            m = build_message("system", "tick", {time:self.ticks,
                diff:diff})
            self.bus.publish(self, m)
            time.sleep(100)

if __name__ == '__main__':
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

        def notify(self, message, result):
            if result == True:
                print("Success!")

    class __AlwaysSubscriber:
        def __init__(self, bus):
            bus.subscribe_all(self)
            assert(self in bus.always)

        def __call__(self, message):
            print("Got always")
            return True
    import doctest
    doctest.testmod()
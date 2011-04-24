from __future__ import with_statement
import threading

class Event(object):
    "Functor for event-based programming."
    def __init__(self):
        self.handlers = []
        self.lock = threading.Lock()

    def __call__(self, handler):
        self.handlers.append(handler)

    def trigger(self, *args):
        with self.lock:
            for handler in self.handlers:
                handler(*args)

class OnChange(object):
    "Functor for triggering an event when the output of a function changes."
    def __init__(self, func, event):
        self.func = func
        self.event = event
        self.last_value = None

    def __call__(self):
        value = self.func()
        if value != self.last_value:
            self.event.trigger()
        self.last_value = value

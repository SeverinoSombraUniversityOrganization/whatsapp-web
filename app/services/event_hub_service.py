class EventHub:
    def __init__(self):
        self._listeners = {}

    def on(self, event, listener):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(listener)

    def emit(self, event, *args, **kwargs):
        if event in self._listeners:
            for listener in self._listeners[event]:
                listener(*args, **kwargs)

    def trigger_event(self, event, *args):
        if event in self._listeners.keys():
            self.emit(event, *args)


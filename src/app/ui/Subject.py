from __future__ import annotations
import app.ui.Observer as observer

class Subject:
    def __init__(self):
        self._observers: list[observer.Observer] = []

    def attach(self, observer: observer.Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: observer.Observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for _observer in self._observers:
            _observer.update(self)
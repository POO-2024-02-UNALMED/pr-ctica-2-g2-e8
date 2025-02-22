
from __future__ import annotations
from abc import ABC, abstractmethod
import app.ui.Subject as subject

class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """

    @abstractmethod
    def update(self, subject: subject.Subject) -> None:...
from app.ui.Observer import Observer
from app.ui.DropdownPublisher import DropdownPublisher
from collections.abc import Callable


class EventListener(Observer):
    def __init__(
        self,
        on_change: Callable[[str], None],
    ) -> None:
        self._on_change = on_change

    def update(self, subject: DropdownPublisher) -> None:
        current_selection = subject.state
        self._on_change(current_selection)

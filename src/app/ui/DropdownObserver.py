from app.ui.Observer import Observer
from app.ui.DropdownPublisher import DropdownPublisher
from collections.abc import Callable, Generator


class DropdownObserver(Observer):
    def __init__(
        self,
        dropdown: DropdownPublisher,
        set_values: Callable[[str], Generator[str, None, None]] | None = None,
    ) -> None:
        self._dropdown = dropdown
        self._set_values = set_values or (lambda _: [])

    def update(self, subject: DropdownPublisher) -> None:
        self._dropdown.set("")
        self._dropdown.configure(values=tuple(self._set_values(subject.state)))

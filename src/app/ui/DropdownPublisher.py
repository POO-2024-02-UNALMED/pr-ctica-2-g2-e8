from app.ui.Subject import Subject
from tkinter import StringVar, ttk, Label, X, Misc


class DropdownPublisher(Subject, ttk.Combobox):
    def __init__(
        self,
        root: Misc,
        label: str,
        initial_values: list[str],
    ) -> None:
        ttk.Combobox.__init__(self, root, values=initial_values, state="readonly")
        Subject.__init__(self)
        self._state: StringVar = StringVar()
        Label(root, text=label).pack(fill=X, padx=5, pady=5)
        self.pack(fill=X, padx=5, pady=5)
        self.bind("<<ComboboxSelected>>", lambda _: self.set_state(self.get()))

    @property
    def state(self) -> str:
        return self._state.get()

    @state.setter
    def state(self, new_state: str) -> None:
        if new_state == self._state.get():
            return
        self._state.set(new_state)
        self.notify()

    def set_state(self, new_state: str) -> None:
        self.state = new_state

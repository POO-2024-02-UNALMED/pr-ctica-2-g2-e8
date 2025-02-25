from .Style import Style

from app.ui.Subject import Subject

from tkinter import StringVar, ttk, Label, X, Misc
from collections.abc import Generator, Callable


class DropdownPublisher(Subject, ttk.Combobox):
    def __init__(
        self,
        root: Misc,
        label: str,
        get_values: Callable[[str | None], Generator[str, None, None] | tuple[str,...]],
    ) -> None:
        ttk.Combobox.__init__(self, root, values=tuple(get_values(None)), state="readonly")
        Subject.__init__(self)
        self._get_values = get_values
        self._state: StringVar = StringVar()
        Label(root, text=label, font=Style.FONT, bg=Style.BG_COLOR, fg=Style.FG_COLOR).pack(fill=X, padx=Style.GAP, pady=Style.GAP)
        self.pack(fill=X, padx=Style.GAP, pady=Style.GAP)
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
        self["values"] = tuple(self._get_values(self.state))

    def clear(self) -> None:
        self.set_state("")
        self.set("")

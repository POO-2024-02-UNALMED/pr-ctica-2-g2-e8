from __future__ import annotations
from tkinter import Frame, Label, Entry
from .Input import Input

class FieldFrame(Frame):
    def __init__(
            self,
            master: Frame,
            criteria_title: str,
            inputs_title: str,
            inputs: tuple[Input, ...],
        ) -> None:
        super().__init__(master, bg="white", bd=1, relief="solid")
        self._criteria_title = criteria_title
        self._inputs_title = inputs_title
        self._inputs = inputs
        self._entries: list[Entry] = []

    def create_grid(self) -> None:
        Label(
            self,
            text=self.criteria_title,
            bg="white"
        ).grid(row=0, column=0, columnspan=2, sticky="w")
        Label(
            self,
            text=self.inputs_title,
            bg="white"
        ).grid(row=1, column=0, columnspan=2, sticky="w")
        self.grid(row=0, column=0, sticky="w")

        for i, input in enumerate(self._inputs):
            Label(self, text=input.label, bg="white").grid(row=i+2, column=0, sticky="w")

            entry = Entry(self, bg="white")
            entry.grid(row=i+2, column=1, sticky="w")
            if input_value := input.get_value():
                entry.insert(0, str(input_value))
            entry.config(state="disable" if input.is_disabled() else "normal")

            self._entries.append(entry)
            input.set_entry_ref(entry)


    def get_values(self) -> tuple[tuple[str, str | int | float | None], ...]:
        return tuple(input.get_label_value_pair() for input in self._inputs)

    def get_value(self, label: str) -> str | int | float | None:
        _input = next(filter(lambda x: x.get_label() == label, self._inputs), None)
        return _input.get_value() if _input else None
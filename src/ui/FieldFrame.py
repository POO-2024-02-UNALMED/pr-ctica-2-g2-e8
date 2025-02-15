from __future__ import annotations

from ..app_management.exceptions import InvalidInputType, InputValueNotProvided
from .Input import Input

from collections.abc import Callable
from tkinter import Frame, Label, Entry, Button, Event, messagebox

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
        self._submit_button: Button | None = None
        self._reset_button: Button | None = None
        self.create_grid()
        self.add_submit_and_reset_buttons(self.handle_submit, self.handle_reset)

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
            entry.config(state="disabled" if input.is_disabled() else "normal")

            self._entries.append(entry)
            input.set_entry_ref(entry)

    def add_submit_and_reset_buttons(
        self,
        submit_command: Callable[[Event[Button]], object],
        reset_command: Callable[[Event[Button]], object]
    ) -> None:
        submit_button = Button(
            self,
            text="Submit",
            bg="white"
        )
        submit_button.bind("<Button-1>", lambda e: submit_command(e))
        self._submit_button = submit_button
        submit_button.grid(row=len(self._inputs)+2, column=0, sticky="w")

        reset_button = Button(
            self,
            text="Reset",
            bg="white"
        )
        reset_button.bind("<Button-1>", lambda e: reset_command(e))
        self._reset_button = reset_button
        reset_button.grid(row=len(self._inputs)+2, column=1, sticky="w")

    def handle_reset(self, _: Event[Button]) -> Button:
        for entry in self._entries:
            if entry["state"] != "disabled":
                entry.delete(0, "end")

        return self._reset_button

    def handle_submit(self, _: Event[Button]) -> Button:
        for input in self._inputs:
            try:
                input.set_value()
            except (InputValueNotProvided, InvalidInputType) as e:
                messagebox.showerror("Error", str(e))

        return self._submit_button

    def get_values(self) -> tuple[tuple[str, str | int | float | None], ...]:
        return tuple(input.get_label_value_pair() for input in self._inputs)

    def get_value(self, label: str) -> str | int | float | None:
        _input = next(filter(lambda x: x.get_label() == label, self._inputs), None)
        return _input.get_value() if _input else None

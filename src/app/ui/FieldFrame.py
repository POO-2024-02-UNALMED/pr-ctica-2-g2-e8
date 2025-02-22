from __future__ import annotations

from app.classes.exceptions import AppException
from app.ui.Input import Input

from collections.abc import Callable
from tkinter import Frame, Label, Entry, Button, Event, messagebox
from typing import Final


class FieldFrame(Frame):
    _BG_COLOR: Final = "#1d2433"
    _FONT: Final = ("Helvetica", 12)
    _GAP: Final = 5

    def __init__(
        self,
        master: Frame,
        title: str,
        description: str,
        criteria_title: str,
        inputs_title: str,
        inputs: tuple[Input, ...],
    ) -> None:
        super().__init__(
            master, bg=FieldFrame._BG_COLOR, bd=1, relief="solid", padx=10, pady=10
        )
        self._criteria_title = criteria_title
        self._inputs_title = inputs_title
        self._inputs = inputs
        self._entries: list[Entry] = []
        self._submit_button: Button | None = None
        self._reset_button: Button | None = None

        master.grid_rowconfigure(0, weight=1)
        master.grid_columnconfigure(0, weight=1)

        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        Label(self, text=title, bg=FieldFrame._BG_COLOR, font=FieldFrame._FONT).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )
        Label(
            self,
            text=description,
            bg=FieldFrame._BG_COLOR,
            font=FieldFrame._FONT,
            pady=30,
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )
        self.create_grid()
        self.add_submit_and_reset_buttons(self._handle_submit, self._handle_reset)

    def create_grid(self) -> None:
        Label(
            self,
            text=self._criteria_title,
            bg=FieldFrame._BG_COLOR,
            font=FieldFrame._FONT,
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )
        Label(
            self,
            text=self._inputs_title,
            bg=FieldFrame._BG_COLOR,
            font=FieldFrame._FONT,
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )
        self.grid(row=0, column=0, sticky="nsew")

        for i, input in enumerate(self._inputs):
            Label(
                self,
                text=input.get_label(),
                bg=FieldFrame._BG_COLOR,
                font=FieldFrame._FONT,
            ).grid(
                row=i + 2,
                column=0,
                sticky="w",
                pady=FieldFrame._GAP,
                padx=FieldFrame._GAP,
            )

            entry = Entry(self, bg="#161a26", font=FieldFrame._FONT)
            entry.grid(
                row=i + 2,
                column=1,
                sticky="nsew",
                pady=FieldFrame._GAP,
                padx=FieldFrame._GAP,
            )
            if input_value := input.get_value():
                entry.insert(0, str(input_value))
            entry.config(state="disabled" if input.is_disabled() else "normal")

            self._entries.append(entry)
            input.set_entry_ref(entry)

    def add_submit_and_reset_buttons(
        self,
        submit_command: Callable[[Event[Button]], object],
        reset_command: Callable[[Event[Button]], object],
    ) -> None:
        button_frame = Frame(self, bg=FieldFrame._BG_COLOR)
        button_frame.grid(
            row=len(self._inputs) + 2,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        submit_button = Button(
            button_frame,
            text="Submit",
            font=FieldFrame._FONT,
            bg="#b36af7",
        )
        submit_button.bind("<Button-1>", lambda e: submit_command(e))
        self._submit_button = submit_button
        submit_button.grid(row=0, column=0, sticky="nsew")

        reset_button = Button(button_frame, text="Reset", font=FieldFrame._FONT)
        reset_button.bind("<Button-1>", lambda e: reset_command(e))
        self._reset_button = reset_button
        reset_button.grid(row=0, column=1, sticky="nsew")

    def _handle_reset(self, _: Event[Button]) -> Button:
        for entry in self._entries:
            if entry["state"] != "disabled":
                entry.delete(0, "end")

        return self._reset_button

    def _handle_submit(self, _: Event[Button]) -> Button:
        for input in self._inputs:
            try:
                input.set_value()
            except AppException as e:
                messagebox.showerror("Error", str(e))
                break

        # clear the entry fields
        for entry in self._entries:
            entry.delete(0, "end")

        return self._submit_button

    def get_values(self) -> tuple[tuple[str, str | int | float | None], ...]:
        return tuple(input.get_label_value_pair() for input in self._inputs)

    def get_value(self, label: str) -> str | int | float | None:
        _input = next(filter(lambda x: x.get_label() == label, self._inputs), None)
        return _input.get_value() if _input else None

    def get_submit_button(self) -> Button:
        return self._submit_button

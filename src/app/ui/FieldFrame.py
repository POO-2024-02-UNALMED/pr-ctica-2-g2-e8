from __future__ import annotations

from app.classes.exceptions import AppException
from app.ui.Input import Input

from collections.abc import Callable
from tkinter import Frame, Label, Button, Event, messagebox, TclError
from typing import Final

from .EntryInput import EntryInPut
from .Style import Style

class FieldFrame(Frame):
    _BG_COLOR: Final = Style.BG_COLOR
    _FG_COLOR: Final = Style.FG_COLOR
    _FONT: Final = Style.FONT
    _GAP: Final = Style.GAP

    def __init__(
        self,
        master: Frame,
        title: str,
        description: str,
        criteria_title: str,
        inputs_title: str,
        inputs: tuple[Input, ...],
    ) -> None:
        super().__init__(master, bg=FieldFrame._BG_COLOR, bd=1, relief="solid")
        self._criteria_title = criteria_title
        self._inputs_title = inputs_title
        self._entries: list[EntryInPut] = []
        self._submit_button: Button | None = None
        self._reset_button: Button | None = None

        try:
            master.grid_rowconfigure(0, weight=1)
            master.grid_columnconfigure(0, weight=1)
            self.grid(row=0, column=0, sticky="nsew")
            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(0, weight=1)
        except TclError:
            pass

        Label(
            self,
            text=title,
            bg=FieldFrame._BG_COLOR,
            fg=FieldFrame._FG_COLOR,
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
            text=description,
            bg=FieldFrame._BG_COLOR,
            font=FieldFrame._FONT,
            pady=30,
            fg=FieldFrame._FG_COLOR,
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )
        self.create_grid(inputs)
        self.add_submit_and_reset_buttons(self._handle_submit, self._handle_reset)

    def create_grid(self, inputs: list[Input]) -> None:
        Label(
            self,
            text=self._criteria_title,
            bg=FieldFrame._BG_COLOR,
            font=FieldFrame._FONT,
            fg=FieldFrame._FG_COLOR,
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
            fg=FieldFrame._FG_COLOR,
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=FieldFrame._GAP,
            padx=FieldFrame._GAP,
        )

        for i, input in enumerate(inputs):
            Label(
                self,
                text=input.get_label(),
                bg=FieldFrame._BG_COLOR,
                font=FieldFrame._FONT,
                fg=FieldFrame._FG_COLOR,
            ).grid(
                row=i + 2,
                column=0,
                sticky="w",
                pady=FieldFrame._GAP,
                padx=FieldFrame._GAP,
            )

            entry = EntryInPut[input._value_type](self, input)
            entry.grid(
                row=i + 2,
                column=1,
                sticky="nsew",
                pady=FieldFrame._GAP,
                padx=FieldFrame._GAP,
            )
            self._entries.append(entry)

    def add_submit_and_reset_buttons(
        self,
        submit_command: Callable[[Event[Button]], object],
        reset_command: Callable[[Event[Button]], object],
    ) -> None:
        button_frame = Frame(self, bg=FieldFrame._BG_COLOR)
        button_frame.grid(
            row=len(self._entries) + 2,
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
        for entry in self._entries:
            try:
                entry.get_input().set_value(entry.get())
            except AppException as e:
                messagebox.showerror("Error", str(e))
                break

        return self._submit_button

    def get_values(self) -> tuple[str, str | int | float | None]:
        return tuple(entry.get_value() for entry in self._entries)

    def get_value(self, label: str) -> str | int | float | None:
        _entry = next(
            filter(lambda x: x.get_input().get_label() == label, self._entries), None
        )
        return _entry.get_value() if _entry else None

    def get_submit_button(self) -> Button:
        return self._submit_button

    def reset_entries(self) -> None:
        for entry in self._entries:
            entry.clear()

    def clear(self) -> None:
        self.reset_entries()
        self._submit_button.config(state="normal")
        self._reset_button.config(state="normal")

    def is_valid(self) -> bool:
        return all(entry.is_valid() for entry in self._entries)

from __future__ import annotations

from ..classes.exceptions import InvalidInputType, InputValueNotProvided

from dataclasses import dataclass
from tkinter import Entry
from typing import Literal

TValue = Literal["str", "int", "float"]

@dataclass
class Input():
    _label: str
    _value_type: TValue
    _required: bool = True
    _disable: bool = False
    _value: str | int | float | None = None
    _entry_ref: Entry | None = None
    _is_valid: bool = True
    _error: Exception | None = None

    def set_value(self) -> None:
        """
          Will raise ValueError if value is
          required and not set or if value is not of the correct type
        """
        if not self.validate()._is_valid and self._error:
            raise self._error

        if self._entry_ref:
            self._value = self._cast_to_value_type(self._entry_ref.get())

    def set_entry_ref(self, entry: Entry) -> Input:
        self._entry_ref = entry
        return self

    def get_value(self) -> str | int | float | None:
        return self._value

    def get_label_value_pair(self) -> tuple[str, str | int | float | None]:
        return self._label, self._value

    def get_label(self) -> str:
        return self._label

    def is_disabled(self) -> bool:
        return self._disable

    def _cast_to_value_type(self, value) -> str | int | float | None:
        try:
            if self._value_type == "str":
                return str(value)
            elif self._value_type == "int":
                return int(value)
            elif self._value_type == "float":
                return float(value)
        except ValueError:
            self._is_valid = False
            raise InvalidInputType(
                f"Value of {self._label} should be of type {self.value_type}"
            )
        return None

    def validate(self) -> Input:
        if self._required and self._value is None:
            self._is_valid = False
            self._error = InputValueNotProvided(self._label)

        if self._value_type == "str":
            self._is_valid = isinstance(self._value, str)
        elif self._value_type == "int":
            self._is_valid = isinstance(self._value, int)
        elif self._value_type == "float":
            self._is_valid = isinstance(self._value, float)

        if not self._is_valid:
            self._error = InvalidInputType(
                f"Value of {self._label} should be of type {self._value_type}"
            )
        return self


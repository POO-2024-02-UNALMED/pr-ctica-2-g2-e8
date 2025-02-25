from __future__ import annotations

from app.classes.exceptions import (
    InvalidInputType,
    InputValueNotProvided,
    LengthException,
    NoInRange,
    AppException,
)

from dataclasses import dataclass
from tkinter import Entry

from collections.abc import Callable

TValue = type[str] | type[int] | type[float]
TInputType = int | float | str | None


@dataclass
class Input[T]:
    _label: str
    _value_type: TValue = str
    _required: bool = True
    _disable: bool = False
    _value: T | None = None
    _validations: tuple[Callable[[T], Callable[[str], AppException | None]], ...] = None
    _entry_ref: Entry | None = None
    _error: Exception | None = None

    def set_value(self, value: str) -> None:
        self.value = value
        self._error = None

    def set_entry_ref(self, entry: Entry) -> Input:
        self._entry_ref = entry
        return self

    @property
    def value(self) -> T:
        return self._value

    @value.getter
    def value(self) -> T:
        self.set_value(self._entry_ref.get() if self._entry_ref else self._value)
        return self._value

    @value.setter
    def value(self, value: T | None = None) -> None:
        try:
            self._value = self.validate(value)
            if self._validations:
                for validation in self._validations:
                    if error := validation(self._value)(self._label):
                        raise error
        except AppException as e:
            self._error = e
            raise e

    def get_initial_value(self) -> T:
        return self._value

    def get_label_value_pair(self) -> tuple[str, TInputType]:
        return self._label, self.value

    def get_label(self) -> str:
        return self._label

    def is_disabled(self) -> bool:
        return self._disable

    def get_error(self) -> Exception | None:
        return self._error

    def _cast_to_value_type(self, value: str | None) -> TInputType:
        if not value:
            return None
        try:
            if self._value_type is str:
                return str(value)
            elif self._value_type is int:
                return int(value)
            elif self._value_type is float:
                return float(value)
        except ValueError:
            raise InvalidInputType(
                f"Value of {self._label} should be of type {self._value_type.__name__}"
                f" but got {type(value).__name__} '{value}'"
            )
        return value

    def validate(self, value: T | None) -> TInputType:
        if self._required and not value:
            raise InputValueNotProvided(self._label)

        return self._cast_to_value_type(value)

    def clear(self) -> None:
        if self.is_disabled():
            return

        self._entry_ref.delete(0, "end")
        self._value = None
        self._error = None

    @staticmethod
    def validate_len(
        value: str, min_len: int, max_len: int
    ) -> Callable[[str], AppException | None]:
        def _validate(label: str) -> AppException | None:
            if not min_len <= len(value) <= max_len:
                return LengthException(label, min_len, max_len)

            return None

        return _validate

    @staticmethod
    def validate_in_range(
        value: int | float, min_value: int | None, max_value: int | None
    ) -> Callable[[str], AppException | None]:
        def _validate(label: str) -> AppException | None:
            if not min_value and not max_value:
                return ValueError("Please provide a min or max value")

            if min_value and value < min_value:
                return NoInRange(label, min_value, max_value)
            if max_value and value > max_value:
                return NoInRange(label, min_value, max_value)

            return None

        return _validate

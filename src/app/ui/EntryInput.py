from .Input import Input
from tkinter import Entry

class EntryInPut[T](Entry):
    def __init__(self, master, input: Input[T]) -> None:
        super().__init__(master,  font=("Helvetica", 12))
        input.set_entry_ref(self)
        self._input = input
        if input_value := input.get_initial_value():
            self.insert(0, str(input_value))
        self.config(state="disabled" if input.is_disabled() else "normal")


    def get_value(self) -> T:
        self._input.set_value(self.get())
        return self._input.value

    def set_input_value(self) -> None:
        self._input.set_value(self.get())

    def get_input(self) -> Input[T]:
        return self._input

    def clear(self) -> None:
        self._input.clear()

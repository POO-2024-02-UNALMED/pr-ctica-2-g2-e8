from tkinter import Frame, messagebox, Button
from app.classes.customers import User
from app.ui.DropdownPublisher import DropdownPublisher
from .EventListener import EventListener
from .AddCreditCardProcessor import AddCreditCardProcessor

from collections.abc import Generator


class ChangePaymentMethodProcessor(Frame):
    def __init__(self, user: User, container: Frame) -> None:
        super().__init__(container)
        self._user = user
        self._container = container
        self._subscriptions_dropdown: DropdownPublisher | None = None
        self._payment_method_dropdown: DropdownPublisher | None = None
        self._generator_ref: Generator[None, None, None] | None = None

        self._show_change_payment_method_form()

    def _handle_selection(self, payment_method: str) -> Generator[None, None, None]:
        try:
            selected_subscription = next(
                _subscription
                for _subscription in self._user.get_subscriptions()
                if _subscription.get_plan().get_name()
                == self._subscriptions_dropdown.state
            )
            if payment_method == "Add new credit card":
                frame = Frame(self._container)
                frame.pack()
                add_card_processor = AddCreditCardProcessor(self._user)
                field_frame = add_card_processor.show_add_credit_card_form(frame)
                field_frame.get_submit_button().config(text="Validate Card")
                field_frame.pack()
                yield None
                selected_payment_method = add_card_processor.get_card()
            else:
                yield None
                selected_payment_method = next(
                    _payment_method
                    for _payment_method in self._user.get_payment_methods()
                    if _payment_method.get_description() == payment_method
                )
        except StopIteration:
            messagebox.showerror(
                "Missing Selection",
                "Please fill all fields",
            )
        else:
            self._add_submit_button()
            if not selected_payment_method:
                messagebox.showerror(
                    "Missing Selection",
                    "Please provide a payment method",
                )

            elif selected_subscription.upsert_payment_method(selected_payment_method):
                messagebox.showinfo(
                    "Payment Method",
                    f"Payment method has been updated to {selected_payment_method.get_description()}",
                )
                self._subscriptions_dropdown.clear()

        yield None

    def _show_change_payment_method_form(self) -> None:
        self._subscriptions_dropdown = DropdownPublisher(
            self._container,
            "Select Subscription you want to update REQUIRED",
            (_subs.get_plan().get_name() for _subs in self._user.get_subscriptions()),
        )
        self._payment_method_dropdown = DropdownPublisher(
            self._container,
            "Select the payment method you want to use REQUIRED",
            ("Add new credit card",)
            + tuple(
                payment_method.get_description()
                for payment_method in self._user.get_payment_methods()
            ),
        )

        self._payment_method_dropdown.attach(EventListener(self._set_generator_ref))

    def _set_generator_ref(self, selection: str) -> None:
        self._generator_ref = self._handle_selection(selection)
        return next(self._generator_ref)

    def _add_submit_button(self) -> None:
        def _handle_submit() -> None:
            try:
                next(self._generator_ref)
            except StopIteration:
                self._set_generator_ref(self._payment_method_dropdown.state)
                messagebox.showerror(
                    "Error",
                    "Please select a Subscription",
                )

        is_disabled = not self._subscriptions_dropdown.state or not self._payment_method_dropdown.state

        self._submit_button = Button(
            self._container,
            text="Submit",
            command=lambda: next(_handle_submit),
            state="disabled" if is_disabled else "normal",
        )
        self._submit_button.pack()

    def _enable_submit_button(self) -> None:
        is_disabled = not self._subscriptions_dropdown.state or not self._payment_method_dropdown.state
        self._submit_button.config(state="disabled" if is_disabled else "normal")

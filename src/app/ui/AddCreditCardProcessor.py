from tkinter import Frame, messagebox
from app.classes.customers import User
from app.classes.gateways import GatewaysFactory, Gateway
from app.classes.transactions import Card
from .FieldFrame import FieldFrame
from .Input import Input

from datetime import datetime
from collections.abc import Callable


class AddCreditCardProcessor:
    def __init__(self, user: User) -> None:
        self._user = user
        self._card: Card | None = None

    def _add_card(self, field_frame: FieldFrame) -> Callable[[], None]:
        def _add_card() -> None:
            card = GatewaysFactory.get_gateway(Gateway.PROJECT_GATEWAY).add_credit_card(
                field_frame.get_value("Card Number"),
                field_frame.get_value("Card Holder Name"),
                field_frame.get_value("Expiration Date"),
                field_frame.get_value("Security Code"),
                self._user,
            )

            if not card:
                messagebox.showinfo("Error", "Credit card not added")
                return lambda: None

            self._user.add_credit_card(card)
            messagebox.showinfo("Success", "Credit card added successfully")
            self._card = card
            field_frame.clear()

        return _add_card

    def show_add_credit_card_form(self, container: Frame) -> FieldFrame:
        current_date = datetime.now()
        card_number = Input[int](
            "Card Number",
            int,
            _validations=(lambda x: Input.validate_len(str(x), 5, 16),),
        )
        expiration_date = Input[str](
            "Expiration Date",
            str,
            _validations=(
                lambda x: Input.validate_len(str(x), 5, 5),
                lambda x: Input.validate_in_range(int(x[:2]), 1, 12),
                lambda x: Input.validate_in_range(
                    int(x[3:]), int(str(current_date.year)[2:]), None
                ),
            ),
        )
        security_code = Input[int](
            "Security Code",
            int,
            _validations=(lambda x: Input.validate_len(str(x), 3, 5),),
        )
        card_holder_name = Input[str](
            "Card Holder Name",
            str,
            _validations=(lambda x: Input.validate_len(x, 5, 50),),
        )

        field_frame = FieldFrame(
            container,
            "Add Credit Card",
            "Please enter the following information to add a new credit card",
            "Add Credit Card",
            "Credit Card Information",
            (
                card_number,
                expiration_date,
                security_code,
                card_holder_name,
            ),
        )

        field_frame.get_submit_button().config(
            command=self._add_card(field_frame)
        )

        return field_frame

    def get_card(self) -> Card | None:
        return self._card

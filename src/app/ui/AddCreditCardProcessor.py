from tkinter import Frame
from .FieldFrame import FieldFrame
from .Input import Input

from datetime import datetime


class AddCreditCardProcessor():
    def __init__(self) -> None:...

    @staticmethod
    def show_add_credit_card_form(container: Frame) -> FieldFrame:
        current_date = datetime.now()
        return FieldFrame(
            container,
            "Add Credit Card",
            "Please enter the following information to add a new credit card",
            "Add Credit Card",
            "Credit Card Information",
            (
                Input[int](
                    "Card Number",
                    int,
                    _validations=(lambda x: Input.validate_len(str(x), 5, 16),),
                ),
                Input[str](
                    "Expiration Date",
                    str,
                    _validations=(
                        lambda x: Input.validate_len(str(x), 5, 5),
                        lambda x: Input.validate_in_range(int(x[:2]), 1, 12),
                        lambda x: Input.validate_in_range(
                            int(x[3:]), int(str(current_date.year)[2:]), None
                        ),
                    ),
                ),
                Input[int](
                    "Security Code",
                    int,
                    _validations=(lambda x: Input.validate_len(str(x), 3, 5),),
                ),
                Input[str](
                    "Card Holder Name",
                    str,
                    _validations=(lambda x: Input.validate_len(x, 5, 50),),
                ),
            ),
        )

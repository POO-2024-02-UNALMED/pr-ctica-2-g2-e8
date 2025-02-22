from abc import ABC, abstractmethod
from app.classes.transactions import Transaction, Card
from app.classes.gateways import Gateway

import re


class IGateway(ABC):
    @staticmethod
    @abstractmethod
    def pay(transaction: Transaction): ...

    @abstractmethod
    def add_credit_card(
        self,
        card_number: int,
        card_holder: str,
        expiration_date: str,
        cvv: int,
        user: str,
    ) -> Card | None: ...

    @abstractmethod
    def authenticated(self): ...

    @abstractmethod
    def delete_card(self, card: Card): ...

    def validate(
        self, card_number: int, card_holder: str, expiration_date: str, cvv: int
    ):
        return (
            len(card_number) > 4
            and len(card_holder) > 3
            and re.match("\d{2}/\d{2}", expiration_date)
            and len(cvv) > 2
            and len(cvv) < 5
        )

    @abstractmethod
    def get_name(self) -> Gateway: ...

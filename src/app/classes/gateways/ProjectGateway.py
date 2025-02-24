from .IGateway import IGateway
from .Authenticate import Authenticate
from .Gateway import Gateway
from app.database.Repository import Repository
from app.classes.transactions import Transaction, Card, TransactionStatus
from app.classes.customers import User

import os


class ProjectGateway(Authenticate, IGateway):
    _name = Gateway.PROJECT_GATEWAY

    def __init__(self):
        super().__init__(Gateway.PROJECT_GATEWAY)

    def add_credit_card(
        self,
        card_number: int,
        card_holder: str,
        expiration_date: str,
        cvv: int,
        user: User,
    ) -> Card | None:
        if not self.validate(card_number, card_holder, expiration_date, cvv):
            return None

        card = Card(
            str(card_number)[-4:],
            expiration_date,
            Card.determine_franchise(str(card_number)),
            self.generate_card_token(card_number, card_holder, expiration_date),
            Gateway.PROJECT_GATEWAY,
            user,
        )
        Repository.save(card, "Card" + os.path.sep + user.get_id())
        return card

    def delete_card(self, card: Card) -> bool:
        return True

    def get_name(self) -> Gateway:
        return self._name

    @staticmethod
    def pay(transaction: Transaction) -> Transaction:
        if transaction.get_gateway() != Gateway.PROJECT_GATEWAY:
            return transaction

        transaction.set_status(TransactionStatus.ACCEPTED)
        return transaction

    def authenticated(self) -> bool:
        return self.AUTHENTICATION_TOKEN is not None

    @staticmethod
    def generate_card_token(
        card_number: int, card_holder: str, expiration_date: str
    ) -> str:
        value = str(card_number) + card_holder + expiration_date
        token_builder = ""
        for i in range(len(value)):
            token_builder += str(ord(value[i]))
        return token_builder

from .IGateway import IGateway
from .Authenticate import Authenticate
from .Gateway import Gateway
from database.Repository import Repository
from ..transactions.Card import Card
from ..transactions.TransactionStatus import TransactionStatus

import os

class ProjectGateway(Authenticate, IGateway):
    def __init__(self):
        super().__init__(Gateway.PROJECT_GATEWAY)

    def pay(self, transaction):
        transaction.set_status(TransactionStatus.ACCEPTED)
        return transaction

    def authenticated(self):
        return self.AUTHENTICATION_TOKEN != None

    @staticmethod
    def generate_card_token(card_number, card_holder, expiration_date):
        value = card_number + card_holder + expiration_date
        token_builder = ""
        for i in range(len(value)):
            token_builder += str(ord(value[i]))
        return token_builder

    def add_credit_card(self, card_number, card_holder, expiration_date, cvv, user):
        if not self.validate(card_number, card_holder, expiration_date, cvv):
            return None
        card = Card(
            card_number[-4:],
            expiration_date,
            Card.get_franchise(card_number),
            self.generate_card_token(card_number, card_holder, expiration_date),
            Gateway.PROJECT_GATEWAY,
            user
        )
        Repository.save(card, "Card" + os.path.sep + user.get_id())
        return card

    def delete_card(self, card):
        return True

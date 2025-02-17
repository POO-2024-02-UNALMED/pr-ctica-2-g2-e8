import WithId
from Transactions import TransactionStatus, Card
from database import Repository
from enum import Enum
from abc import ABC
import os

class Gateway(Enum):
    OTHER = "OTHER"
    PROJECT_GATEWAY = "PROJECT_GATEWAY"

class IGateway(ABC):
    def pay(self, transaction):
        pass

    def add_credit_card(self, card_number, card_holder, expiration_date, cvv, user):
        pass

    def authenticated(self):
        pass

    def delete_card(self, card):
        pass

    def validate(self, card_number, card_holder, expiration_date, cvv):
        return len(card_number) > 4 and len(card_holder) > 3 and expiration_date.matches("\d{2}/\d{2}") and len(cvv) > 2 and len(cvv) < 5

class Credential(WithId):
    def __init__(self, public_key, private_key, gateway):
        super().__init__(gateway.get_name())
        self.public_key = public_key
        self.private_key = private_key
        self.gateway = gateway

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def get_gateway(self):
        return self.gateway

class GatewaysFactory:
    def __init__(self, gateway):
        self.gateways = {}
        self.gateway = gateway
        self.initialize_gateway()

    def __init__(self, gatewaysToAdd):
        self.gateways = {}
        self.iterate_and_add(gatewaysToAdd)

    def iterate_and_add(self, gatewaysToAdd):
        for gateway in gatewaysToAdd:
            self.gateways[gateway] = ProjectGateway()

    def get_gateway(self, gateway):
        return self.gateways.get(gateway)

    def initialize_gateway(self, gateway):
        if not self.gateways:
            self.gateways[gateway] = ProjectGateway()
        else:
            self.gateways[gateway] = ProjectGateway()

    def initialize_gateways(self, gatewaysAndCredentials):
        if not self.gateways:
            self.iterate_and_add(gatewaysAndCredentials)
        else:
            self.iterate_and_add(gatewaysAndCredentials)

class Authenticate:
    def __init__(self, gateway):
        credential = Repository.load("Credential", gateway.get_name())
        self.AUTHENTICATION_TOKEN = credential.get_public_key() + credential.get_private_key()

    def get_authentication_token(self):
        return self.AUTHENTICATION_TOKEN

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


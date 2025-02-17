import WithId
from enum import Enum
from datetime import datetime

class TransactionStatus(Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    PENDING = "PENDING"
    CANCELLED = "CANCELLED"
    REVERSED = "REVERSED"

class Franchise(Enum):
    VISA = "VISA"
    MASTERCARD = "MASTERCARD"
    AMERICAN_EXPRESS = "AMERICAN EXPRESS"
    DINERS_CLUB = "DINERS CLUB"
    DISCOVER = "DISCOVER"
    JCB = "JCB"
    UNIONPAY = "UNIONPAY"
    MAESTRO = "MAESTRO"
    VISA_ELECTRON = "VISA_ELECTRON"
    V_PAY = "V_PAY"
    MIR = "MIR"
    TROY = "TROY"
    UATP = "UATP"
    UNKNOWN = "UNKNOWN"

class Transaction(WithId):
    def __init__(self, description, user, price):
        super().__init__(self.create_id(self.get_month_and_year(), user.get_email()))
        self.description = description
        self.price = price
        self.user_email = user.get_email()
        self.gateway = user.get_gateway()
        self.date = datetime.now()

    def __init__(self, description, user, price, status):
        self(description, user, price)
        self.status = status

    def __init__(self, description, user, price, status, card):
        self(description, user, price, status)
        self.payment_method = card

    def get_payment_method(self):
        return self.payment_method

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_user_email(self):
        return self.user_email

    def get_gateway(self):
        return self.gateway

    def get_date(self):
        return self.date

    @staticmethod
    def get_month_and_year():
        return datetime.now().strftime("%m-%Y")

    @staticmethod
    def create_id(attribute1, attribute2):
        return WithId.create_id(attribute1, attribute2)

class Card(WithId):
    def __init__(self, last_four, due_date, franchise, token, gateway, card_owner):
        super().__init__(self.create_id(due_date, last_four))
        self.due_date = due_date
        self.last_four = last_four
        self.franchise = franchise
        self.token = token
        self.gateway = gateway
        self.card_owner = card_owner

    def get_due_date(self):
        return self.due_date

    def get_last_four(self):
        return self.last_four

    def get_franchise(self):
        return self.franchise

    def get_token(self):
        return self.token

    def delete(self):
        self.gateway.delete_card(self)

    def get_card_owner(self):
        return self.card_owner
    
    @staticmethod
    def get_franchise(number):
        if number.startswith("4"):
            return Franchise.VISA
        elif number.startswith("5"):
            return Franchise.MASTERCARD
        elif number.startswith("6"):
            return Franchise.DISCOVER
        else:
            return Franchise.UNKNOWN
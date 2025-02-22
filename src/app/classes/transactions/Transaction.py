from classes.WithId import WithId

from datetime import datetime

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
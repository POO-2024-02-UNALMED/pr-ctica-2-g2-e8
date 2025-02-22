from app.classes.WithId import WithId
from .Franchise import Franchise

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
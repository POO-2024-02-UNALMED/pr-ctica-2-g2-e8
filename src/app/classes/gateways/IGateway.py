from abc import ABC

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

import WithId
from Plan import Plan, Subscription, SubscriptionStatus
from Transactions import Transaction, TransactionStatus
from Gateways import Credential
from database import Repository
from enum import Enum
from datetime import datetime
import os

class DocumentType(Enum):
    CC = "CC"
    CE = "CE"
    TI = "TI"
    PP = "PP"
    NIT = "NIT"


class Customer(WithId):
    def __init__(self, email, password, document_type, document_number):
        super().__init__(self.create_id(email, password))
        self.email = email
        self.password = password
        self.document_type = document_type
        self.document_number = document_number

    def get_email(self):
        return self.email

    def get_document_type(self):
        return self.document_type

    def get_document_number(self):
        return self.document_number

class Admin(Customer):
    def __init__(self, email, password, document_type, document_number):
        super(email, password, document_type, document_number)

    def create_plan(self, name, description, price):
        plan = Plan(name, description, price)
        Repository.save(plan)
        return plan

    def configure_gateway(self, gateway, public_key, private_key):
        credential = Credential(public_key, private_key, gateway)
        Repository.save(credential)
        return credential

    def inactivate(self, plan):
        Repository.update(plan)

class User(Customer):
    def __init__(self, email, password, document_type, document_number):
        super().__init__(email, password, document_type, document_number)
    
    def change_subscription_payment_method(self, subscription, card):
        subscription.set_payment_method(card)
        transaction = Transaction(
            subscription.get_plan().get_name(),
            subscription.get_user(),
            1,
            TransactionStatus.PENDING
        )
        subscription.process_payment(transaction)
        return transaction.get_status() == TransactionStatus.ACCEPTED
    
    def save_on_repository_and_add_to_subscriptions(self, subscription):
        Repository.save(subscription, "Subscription" + os.path.sep + subscription.get_plan().get_name())
        if self.subscriptions != None:
            self.subscriptions.append(subscription)
        else:
            self.subscriptions = []
            self.subscriptions.append(subscription)

    def add_subscription(self, plan):
        subscription = Subscription(self, plan)
        initial_charge_transaction = None
        if self.has_credit_card():
            initial_charge_transaction = subscription.process_payment()
        self.save_on_repository_and_add_to_subscriptions(subscription)
        return initial_charge_transaction
    
    def add_subscription(self, plan, card):
        subscription = Subscription(self, plan, card)
        initial_charge_transaction = subscription.process_payment()
        self.save_on_repository_and_add_to_subscriptions(subscription)
        return initial_charge_transaction
    
    def get_user_subscribed_plans(self):
        user_subscriptions = self.get_subscriptions()
        plans = []
        for subscription in user_subscriptions:
            plans.append(subscription.get_plan())
        return plans
    
    def get_subscriptions(self):
        plans = Plan.get_all()
        user_subscriptions = []
        for plan in plans:
            id = WithId.create_id(self.email, plan.get_name())
            subscription = Repository.load("Subscription" + os.path.sep + plan.get_name(), id)
            if subscription != None:
                subscription.set_user(self)
                subscription.set_plan(plan)
                if subscription.get_next_charge_date().is_before(datetime.now()):
                    subscription.set_status(SubscriptionStatus.CANCELLED)
                    subscription.set_suspension_date(subscription.get_next_charge_date())
                    subscription.set_next_charge_date(datetime.min)
                    Repository.update(subscription, "Subscription" + os.path.sep + plan.get_name())
                user_subscriptions.append(subscription)
        self.subscriptions = user_subscriptions
        return user_subscriptions
    
    def get_inactive_subscriptions(self):
        inactive_plans = Plan.get_inactive_plans()
        inactive_subscriptions = []
        for plan in inactive_plans:
            id = WithId.create_id(self.email, plan.get_name())
            subscription = Repository.load("Subscription" + os.path.sep + plan.get_name(), id)
            if subscription != None:
                subscription.set_user(self)
                subscription.set_plan(plan)
                inactive_subscriptions.append(subscription)
        return inactive_subscriptions
    
    def has_credit_card(self):
        return len(Repository.load_all_object_in_directory(self.document_number)) > 0

    def add_credit_card(self, card):
        Repository.save(card, "Card" + os.path.sep + self.get_id())
        return True
    
    def remove_credit_card(self, card):
        Repository.delete(card, "Card" + os.path.sep + self.get_id())

    def get_credit_cards(self):
        cards = Repository.load_all_object_in_directory("Card" + os.path.sep + self.get_id())
        user_cards = []
        for card in cards:
            user_cards.append(card)
        return user_cards
    
    def get_gateway(self):
        return self.gateway

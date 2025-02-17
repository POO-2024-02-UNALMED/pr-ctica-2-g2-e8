import WithId
import Transactions
from Gateways import IGateway
from database import Repository
from enum import Enum
from datetime import datetime, timedelta
import os


class PlanStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class SubscriptionStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    CANCELLED = "CANCELLED"
    PENDING = "PENDING"

class Plan(WithId):
    def __init__(self, name, description, price):
        super().__init__(name)
        self.name = name
        self.description = description
        self.price = price
        self.status = PlanStatus.ACTIVE

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    @staticmethod
    def get_all():
        withIdList = Repository.load_all_object_in_directory("Plan")
        planList = []
        for withId in withIdList:
            if isinstance(withId, Plan) and withId.get_status() == PlanStatus.ACTIVE:
                planList.append(withId)
        return planList

    @staticmethod
    def get_inactive_plans():
        withIdList = Repository.load_all_object_in_directory("Plan")
        planList = []
        for withId in withIdList:
            if isinstance(withId, Plan) and withId.get_status() == PlanStatus.INACTIVE:
                planList.append(withId)
        return planList

    @staticmethod
    def get_subscriptions(plan):
        withIdList = Repository.load_all_object_in_directory("Subscription" + os.path.sep + plan.get_name())
        subscriptionList = []
        for withId in withIdList:
            if isinstance(withId, Subscription):
                subscriptionList.append(withId)
        return subscriptionList

    @staticmethod
    def inactivate_subscriptions(plan):
        withIdList = Repository.load_all_object_in_directory("Subscription" + os.path.sep + plan.get_name())
        subscriptionList = []
        for withId in withIdList:
            if isinstance(withId, Subscription):
                withId.set_status(SubscriptionStatus.INACTIVE)
                withId.set_suspension_date(withId.get_next_charge_date())
                withId.set_next_charge_date(datetime.MIN)
                Repository.update(withId, "Subscription" + os.path.sep + plan.get_name())
                subscriptionList.append(withId)
        return subscriptionList
    
    @staticmethod
    def get_plan(name):
        return Repository.load("Plan", name)

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def __str__(self):
        return f"Plan: {self.name}, Description: {self.description}, Price: {self.price}, Status: {self.status}"

    def __repr__(self):
        return f"Plan: {self.name}, Description: {self.description}, Price: {self.price}, Status: {self.status}"

        
class Subscription(WithId):
    def __init__(self, user, plan):
        super().__init__(self.create_id(user.get_email(), plan.get_name()))
        self.user = user
        self.plan = plan
        self.start_date = datetime.now()
        self.next_charge_date = datetime.now()
        self.status = SubscriptionStatus.INACTIVE
        self.number_of_collection_attempts = 0
        self.card = None
        self.suspension_date = datetime.max

    def process_payment(self, transaction):
        IGateway.pay(transaction)
        if transaction.get_status() == Transactions.TransactionStatus.ACCEPTED and self.next_charge_date > datetime.now() + timedelta(days=1):
            remaining_days = self.next_charge_date - datetime.now()
            self.next_charge_date = datetime.now() + timedelta(days=remaining_days)
        elif transaction.get_status() == Transactions.TransactionStatus.ACCEPTED:
            self.next_charge_date = datetime.now() + timedelta(days=30)
            self.status = SubscriptionStatus.ACTIVE
        elif self.number_of_collection_attempts < 3:
            self.next_charge_date = datetime.now() + timedelta(days=1)
            self.status = SubscriptionStatus.PENDING
            self.number_of_collection_attempts += 1
        else:
            self.status = SubscriptionStatus.CANCELLED
        Repository.update(self, "Subscription" + os.path.sep + self.plan.get_name())
        return transaction

    def process_payment(self):
        transaction = Transactions.Transaction(self.plan.get_name(), self.user, self.plan.get_price(), Transactions.TransactionStatus.PENDING, self.get_payment_method())
        return self.process_payment(transaction)

    def upsert_payment_method(self, card):
        self.set_payment_method(card)
        Repository.update(self)
        transaction = Transactions.Transaction(self.plan.get_name(), self.user, 1, Transactions.TransactionStatus.PENDING)
        self.process_payment(transaction)
        return transaction.get_status() == Transactions.TransactionStatus.ACCEPTED

    def get_gateway(self):
        return self.user.get_gateway()

    def get_payment_method(self):
        if self.card == None:
            return self.user.get_credit_cards()[0]
        return self.card

    def get_user(self):
        return self.user

    def set_user(self, user):
        self.user = user

    def get_plan(self):
        return self.plan

    def set_plan(self, plan):
        self.plan = plan

    def get_next_charge_date(self):
        return self.next_charge
    
    def get_status(self):
        return self.status
    
    def set_status(self, status):    
        self.status = status
    
    def get_start_date(self):  
        return self.start_date
    
    def set_next_charge_date(self, next_charge_date):
        self.next_charge_date = next_charge_date
    
    def set_suspension_date(self, date):
        self.suspension_date = date
    
    def get_suspension_date(self):
        return self.suspension_date
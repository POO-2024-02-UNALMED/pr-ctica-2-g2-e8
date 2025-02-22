from .Customer import Customer
from ..plans.Plan import Plan
from ..plans.Subscription import Subscription
from ..transactions.Transaction import Transaction
from ..transactions.TransactionStatus import TransactionStatus
from ..plans.SubscriptionStatus import SubscriptionStatus
from classes.WithId import WithId
from ...database.Repository import Repository

import os
from datetime import datetime

class User(Customer):
    def __init__(self, email, password, document_type, document_number):
        super().__init__(email, password, document_type, document_number)

    def change_subscription_payment_method(self, subscription, card):
        subscription.set_payment_method(card)
        transaction = Transaction(
            subscription.get_plan().get_name(),
            subscription.get_user(),
            1,
            TransactionStatus.PENDING,
        )
        subscription.process_payment(transaction)
        return transaction.get_status() == TransactionStatus.ACCEPTED

    def save_on_repository_and_add_to_subscriptions(self, subscription):
        Repository.save(
            subscription,
            "Subscription" + os.path.sep + subscription.get_plan().get_name(),
        )
        if self.subscriptions:
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
            _id = WithId.create_id(self.email, plan.get_name())
            subscription = Repository.load(
                "Subscription" + os.path.sep + plan.get_name(), _id
            )
            if subscription:
                subscription.set_user(self)
                subscription.set_plan(plan)
                if subscription.get_next_charge_date().is_before(datetime.now()):
                    subscription.set_status(SubscriptionStatus.CANCELLED)
                    subscription.set_suspension_date(
                        subscription.get_next_charge_date()
                    )
                    subscription.set_next_charge_date(datetime.min)
                    Repository.update(
                        subscription, "Subscription" + os.path.sep + plan.get_name()
                    )
                user_subscriptions.append(subscription)
        self.subscriptions = user_subscriptions
        return user_subscriptions

    def get_inactive_subscriptions(self):
        inactive_plans = Plan.get_inactive_plans()
        inactive_subscriptions = []
        for plan in inactive_plans:
            _id = WithId.create_id(self.email, plan.get_name())
            subscription = Repository.load(
                "Subscription" + os.path.sep + plan.get_name(), _id
            )
            if subscription:
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
        cards = Repository.load_all_object_in_directory(
            "Card" + os.path.sep + self.get_id()
        )
        user_cards = []
        for card in cards:
            user_cards.append(card)
        return user_cards

    def get_gateway(self):
        return self.gateway
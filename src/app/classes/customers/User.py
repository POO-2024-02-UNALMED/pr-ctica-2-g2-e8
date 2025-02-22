from .Customer import Customer
from ..plans.Plan import Plan
from app.classes.plans.Subscription import Subscription, SubscriptionStatus
from app.classes.transactions import Card, Transaction
from app.classes.WithId import WithId
from ...database.Repository import Repository
from app.classes.customers import DocumentType

from typing import cast

import os
from datetime import datetime


class User(Customer):
    def __init__(
        self,
        email: str,
        password: str,
        document_type: DocumentType,
        document_number: int,
    ):
        super().__init__(email, password, document_type, document_number)
        self.subscriptions = []

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

    def add_subscription(self, plan: Plan, card: Card | None = None) -> Transaction:
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
            if isinstance(Subscription, subscription):
                subscription = cast(Subscription, subscription)
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
        return "ProjectGateway"

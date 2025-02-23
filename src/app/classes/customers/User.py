from app.classes.plans import Subscription, SubscriptionStatus, Plan
from app.classes.transactions import Card, Transaction
from app.classes.WithId import WithId
from app.database.Repository import Repository
from app.classes.customers import DocumentType, Customer
from app.classes.gateways import Gateway

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
        gateway: Gateway,
    ):
        super().__init__(email, password, document_type, document_number)
        self._subscriptions: tuple[Subscription, ...] = tuple()
        self._gateway = gateway

    def save_on_repository_and_add_to_subscriptions(self, subscription):
        Repository.save(
            subscription,
            Subscription.DB_PATH + os.path.sep + subscription.get_plan().get_name(),
        )
        self._subscriptions = (*self._subscriptions, subscription)

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

    def _load_subscription(self, plan: Plan) -> Subscription | None:
        subscription = Repository.load(
            Subscription.DB_PATH + os.path.sep + plan.get_name(),
            WithId.create_id(self._email, plan.get_name()),
        )
        if not subscription:
            return None

        subscription = cast(Subscription, subscription)
        subscription.set_user(self)
        subscription.set_plan(plan)
        if subscription.get_next_charge_date().timestamp() < datetime.now().timestamp():
            subscription.set_status(SubscriptionStatus.CANCELLED)
            subscription.set_suspension_date(subscription.get_next_charge_date())
            subscription.set_next_charge_date(datetime.min)
            Repository.update(
                subscription,
                Subscription.DB_PATH + os.path.sep + plan.get_name(),
            )
        return subscription

    def get_subscriptions(self) -> tuple[Subscription, ...]:
        plans = Plan.get_all()
        user_subscriptions = (
            self._load_subscription(plan) for plan in plans
        )
        self._subscriptions = tuple(subs for subs in user_subscriptions if subs)
        return self._subscriptions

    def get_inactive_subscriptions(self):
        inactive_plans = Plan.get_inactive_plans()
        inactive_subscriptions = []
        for plan in inactive_plans:
            _id = WithId.create_id(self._email, plan.get_name())
            subscription = Repository.load(
                Subscription.DB_PATH + os.path.sep + plan.get_name(), _id
            )
            if subscription:
                subscription.set_user(self)
                subscription.set_plan(plan)
                inactive_subscriptions.append(subscription)
        return inactive_subscriptions

    def has_credit_card(self):
        return len(Repository.load_all_object_in_directory(self._document_number)) > 0

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

    def get_gateway(self) -> Gateway:
        return self._gateway

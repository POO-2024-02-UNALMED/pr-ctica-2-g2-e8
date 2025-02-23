from __future__ import annotations

from app.classes.gateways import GatewaysFactory

from app.classes.WithId import WithId
from app.classes.transactions import TransactionStatus, Transaction
from .SubscriptionStatus import SubscriptionStatus
from app.database import Repository
from app.classes.plans import Plan
from app.classes.transactions import Card
from app.classes.customers import User
from typing import Final
from datetime import datetime, timedelta, date
import os


class Subscription(WithId):
    DB_PATH: Final = "Subscriptions"

    def __init__(self, user: User, plan: Plan, card: Card | None = None):
        super().__init__(self.create_id(user.get_email(), plan.get_name()))
        self._user: User = user
        self._plan: Plan = plan
        self.start_date: datetime = datetime.now()
        self.next_charge_date: datetime = datetime.now()
        self.status: Subscription = SubscriptionStatus.INACTIVE
        self.number_of_collection_attempts: int = 0
        self._card = card
        self.suspension_date: datetime = datetime.max
        self._pending_transactions: tuple[Transaction, ...] = tuple()

    def process_payment(
        self, transaction: Transaction | None = None, number_of_installments: int = 1
    ) -> Transaction:
        if not transaction:
            transaction = Transaction(
                self._plan,
                self._user,
                self._plan.get_price(),
                TransactionStatus.PENDING,
                self.get_payment_methods()[0],
            )
        GatewaysFactory.get_gateway(transaction.get_gateway()).pay(transaction)
        if (
            transaction.get_status() == TransactionStatus.ACCEPTED
            and self.next_charge_date > datetime.now() + timedelta(days=1)
        ):
            remaining_days = self.next_charge_date - datetime.now()
            self.next_charge_date = datetime.now() + remaining_days
        elif transaction.get_status() == TransactionStatus.ACCEPTED:
            self.next_charge_date = datetime.now() + timedelta(days=30)
            self.status = SubscriptionStatus.ACTIVE
        elif self.number_of_collection_attempts < 3:
            self.next_charge_date = datetime.now() + timedelta(days=1)
            self.status = SubscriptionStatus.PENDING
            self.number_of_collection_attempts += 1
        else:
            self.status = SubscriptionStatus.CANCELLED

        Repository.update(
            self, Subscription.DB_PATH + os.path.sep + self._plan.get_name()
        )
        self._handle_installments(transaction, number_of_installments)
        return transaction

    def _handle_installments(
        self, transaction: Transaction, number_of_installments: int
    ):
        pending_transactions = (
            Transaction(
                self._plan,
                self._user,
                self._plan.get_price() / number_of_installments,
                transaction.get_payment_method(),
                TransactionStatus.PENDING,
                date.today() + timedelta(days=30 * (i + 1)),
            )
            for i in range(1, number_of_installments - 1)
            if number_of_installments > 1
        )

        if transaction.get_status() != TransactionStatus.ACCEPTED:
            transaction.set_charge_date(date.today() + timedelta(days=1))
            self._pending_transactions = (
                *self._pending_transactions,
                *pending_transactions,
                transaction,
            )

        else:
            self._pending_transactions = (*self._pending_transactions, transaction)

    def upsert_payment_method(self, card):
        self.set_payment_method(card)
        Repository.update(self)
        transaction = Transaction(self._plan, self._user, 1, TransactionStatus.PENDING)
        self.process_payment(transaction)
        return transaction.get_status() == TransactionStatus.ACCEPTED

    def get_gateway(self):
        return self._user.get_gateway()

    def get_payment_methods(self) -> tuple[Card, ...]:
        if not self._card:
            return tuple(self._user.get_credit_cards())
        return (self._card,)

    def get_user(self):
        return self._user

    def set_user(self, user):
        self._user = user

    def get_plan(self) -> Plan:
        return self._plan

    def set_plan(self, plan: Plan):
        self._plan = plan

    def get_next_charge_date(self):
        return self.next_charge_date

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

    def get_pending_transactions(self) -> tuple[Transaction, ...]:
        return self._pending_transactions

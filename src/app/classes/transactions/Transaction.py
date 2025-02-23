from app.classes.WithId import WithId
from app.classes.customers import User
from app.classes.transactions import Card, TransactionStatus
from app.classes.plans import Plan
from app.classes.gateways import Gateway

from datetime import datetime, date


class Transaction(WithId):
    def __init__(
        self,
        plan: Plan,
        user: User,
        total: float,
        payment_method: Card,
        status: TransactionStatus,
        charge_date: date | None = None,
    ) -> None:
        super().__init__(
            WithId.create_id(
                self.get_month_and_year(charge_date or date.today()),
                f"{user.get_email()}-{plan.get_name()}",
            )
        )
        self._value: float = total
        self._user_email: str = user.get_email()
        self._gateway: Gateway = user.get_gateway()
        self._date: datetime = datetime.now()
        self._payment_method: Card = payment_method
        self._status: TransactionStatus = status
        self._charge_date: date = charge_date or date.today()

    def get_payment_method(self) -> Card:
        return self._payment_method

    def set_payment_method(self, payment_method: Card) -> None:
        self._payment_method = payment_method

    def get_status(self) -> TransactionStatus:
        return self._status

    def set_status(self, status):
        self._status = status

    def get_total(self) -> float:
        return self._value

    def get_user_email(self) -> str:
        return self._user_email

    def get_gateway(self) -> Gateway:
        return self._gateway

    def get_date(self) -> datetime:
        return self._date

    def get_charge_date(self) -> datetime:
        return self._charge_date

    def set_charge_date(self, charge_date: date) -> None:
        self._charge_date = charge_date

    @staticmethod
    def get_month_and_year(date: date) -> str:
        return f"{date.year}-{date.month}"

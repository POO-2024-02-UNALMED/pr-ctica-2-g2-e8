from collections.abc import Generator
from tkinter import ttk, Label, Frame, messagebox
from app.ui.DropdownPublisher import DropdownPublisher
from app.ui.DropdownObserver import DropdownObserver
from app.classes.transactions import Transaction, TransactionStatus
from app.classes.customers import User
from app.classes.plans import Subscription


class SubscriptionPaymentProcessor(Frame):
    def __init__(self, user: User, container: Frame) -> None:
        super().__init__(container)
        self._user = user
        self._container = container
        self._subscriptions = self._user.get_subscriptions()
        self._selected_subscription: Subscription | None = None
        self._subscriptions_dropdown: DropdownPublisher | None = None
        self._payment_method_dropdown: DropdownPublisher | None = None
        self._number_of_payments_dropdown: DropdownPublisher | None = None

        self._show_pay_subscription_form()

    def _get_payments_values(
        self,
        subscription_plan_name: str,
    ) -> Generator[str, None, None]:
        selected_subscription = next(
            _subscription
            for _subscription in self._subscriptions
            if _subscription.get_plan().get_name() == subscription_plan_name
        )
        return (
            f"{i} - {selected_subscription.get_plan().get_price() / i}"
            for i in range(1, 5)
        )

    def _get_subscription_payment_methods(
        self,
        subscription_plan_name: str,
    ) -> Generator[str, None, None]:
        self._selected_subscription = next(
            _subscription
            for _subscription in self._subscriptions
            if _subscription.get_plan().get_name() == subscription_plan_name
        )
        return (
            card.get_description()
            for card in self._selected_subscription.get_payment_methods()
        )

    def _show_pay_subscription_form(self) -> None:
        self._subscriptions_dropdown = DropdownPublisher(
            self._container,
            "Select Subscription REQUIRED",
            (_subs.get_plan().get_name() for _subs in self._subscriptions),
        )

        self._payment_method_dropdown = DropdownPublisher(
            self._container,
            "Select the payment method REQUIRED",
            (_ for _ in ()),
        )

        self._number_of_payments_dropdown = DropdownPublisher(
            self._container,
            "Number of payments REQUIRED",
            (_ for _ in ()),
        )

        self._subscriptions_dropdown.attach(
            DropdownObserver(
                self._payment_method_dropdown,
                lambda subscription: self._get_subscription_payment_methods(
                    subscription
                ),
            )
        )

        self._subscriptions_dropdown.attach(
            DropdownObserver(
                self._number_of_payments_dropdown,
                lambda selection: self._get_payments_values(selection),
            )
        )
        ttk.Button(self._container, text="Pay", command=self._handle_submit).pack()

    def _handle_submit(self) -> None:
        try:
            self._process_payment()
        except StopIteration:
            messagebox.showerror("Error", "Please fill all the required fields")


    def _process_payment(self) -> None:
        subscription = next(
            _subs
            for _subs in self._subscriptions
            if _subs.get_plan().get_name() == self._subscriptions_dropdown.state
        )
        payment_method = next(
            card
            for card in subscription.get_payment_methods()
            if card.get_description()
            == self._payment_method_dropdown.state
        )
        number_of_payments = int(
            self._number_of_payments_dropdown.state.split(" - ")[0].strip()
        )
        transaction = Transaction(
            subscription.get_plan(),
            self._user,
            subscription.get_plan().get_price() / number_of_payments,
            payment_method,
            TransactionStatus.PENDING,
        )
        subscription.process_payment(transaction, number_of_payments)

        if transaction.get_status() == TransactionStatus.ACCEPTED:
            plan_name = subscription.get_plan().get_name()
            Label(
                self._container,
                text=f"Payment of {plan_name} has been processed",
            ).pack()
        else:
            Label(self._container, text="Payment has been rejected").pack()

        if (
            number_of_payments > 1
            or transaction.get_status() != TransactionStatus.ACCEPTED
        ):
            for _transaction in subscription.get_pending_transactions():
                Label(
                    self._container,
                    text=(
                        f"Next charge date: {_transaction.get_charge_date()} total: {_transaction.get_total()}"
                        f"- plan: {subscription.get_plan().get_name()}"
                    ),
                ).pack()

        self._number_of_payments_dropdown.clear()
        self._payment_method_dropdown.clear()

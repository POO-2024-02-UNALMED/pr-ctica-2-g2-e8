from tkinter import ttk, Label, Frame, messagebox, Text
from collections.abc import Generator

from .DropdownPublisher import DropdownPublisher
from .DropdownObserver import DropdownObserver
from .Style import Style

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
        self._message: Text = Text(
            self._container,
            wrap="word",
            pady=Style.GAP,
            font=Style.FONT,
            bg=Style.BG_COLOR,
            fg=Style.FG_COLOR,
        )

        self._show_informative_banner()
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
            "Select Subscription",
            lambda _: (_subs.get_plan().get_name() for _subs in self._subscriptions),
        )

        self._payment_method_dropdown = DropdownPublisher(
            self._container,
            "Select the payment method",
            lambda _: (_ for _ in ()),
        )

        self._number_of_payments_dropdown = DropdownPublisher(
            self._container,
            "Number of payments",
            lambda _: (_ for _ in ()),
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
            if card.get_description() == self._payment_method_dropdown.state
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

        self._message.config(state="normal")
        self._message.delete("1.0", "end")
        if transaction.get_status() == TransactionStatus.ACCEPTED:
            plan_name = subscription.get_plan().get_name()
            self._message.insert("end", f"Payment of {plan_name} has been processed \n")
        else:
            self._message.insert(
                "end",
                f"Payment of {subscription.get_plan().get_name()} has been scheduled \n",
            )

        if (
            number_of_payments > 1
            or transaction.get_status() != TransactionStatus.ACCEPTED
        ):
            self._message.config(state="normal")
            self._message.delete("1.0", "end")
            for _transaction in subscription.get_pending_transactions():
                self._message.insert(
                    "end",
                    (
                        f"Next charge date: {_transaction.get_charge_date()} "
                        f"total: {_transaction.get_total()} "
                        f"- plan: {subscription.get_plan().get_name()} \n"
                    ),
                )
                self._message.pack()

        self._message.config(state="disabled")
        self._number_of_payments_dropdown.clear()
        self._payment_method_dropdown.clear()

    def _show_informative_banner(self) -> None:
        text = Text(
            self._container, wrap="word", bg=Style.BG_COLOR, height=6, font=Style.FONT
        )
        text.insert(
            "end",
            "Pay Subscription\n"
            "Select the subscription you want to pay and the payment method you want to use"
            "You can also select the number of payments you want to make"
            "If you select more than one payment, the total will be divided into equal parts",
        )
        text.pack()
        text.config(state="disabled", fg=Style.FG_COLOR)

from tkinter import Frame, messagebox, Button, Text
from app.classes.plans import Plan
from app.classes.customers import User
from app.classes.transactions import TransactionStatus

from .DropdownPublisher import DropdownPublisher
from .Style import Style
from .EventListener import EventListener


class AddSubscriptionProcessor(Frame):
    def __init__(self, user: User, container: Frame) -> None:
        super().__init__(container)
        self._user = user
        self._container = container
        self._pan_selector: DropdownPublisher | None = None
        self._payment_method_selector: DropdownPublisher | None = None
        self._confirm: DropdownPublisher | None = None
        self._submit_button: Button = Button(self._container, text="Pay", state="disabled")

        self._show_informative_banner()
        self._show_add_subscription_form()

    def _handle_submit(self) -> None:
        if self._confirm.state != "Yes":
            messagebox.showinfo("Error", "Confirmation is required")
            return

        try:
            plan = Plan.get_plan(self._pan_selector.state)
            if not plan:
                messagebox.showinfo("Error", "Plan not found")
                return

            payment_method = next(
                (
                    payment_method
                    for payment_method in self._user.get_payment_methods()
                    if payment_method.get_description()
                    == self._payment_method_selector.state
                )
            )
            if (
                self._user.add_subscription(plan, payment_method).get_status()
                == TransactionStatus.ACCEPTED
            ):
                messagebox.showinfo("Success", "Subscription added successfully")
            else:
                messagebox.showinfo("Error", "Subscription not added")
        except StopIteration:
            messagebox.showinfo("Error", "Select payment method")
        else:
            self._pan_selector.clear()
            self._payment_method_selector.clear()
            self._confirm.clear()

    def _show_add_subscription_form(self) -> None:
        subscribed_plans = self._user.get_user_subscribed_plans()
        plans = tuple(plan.get_name() for plan in Plan.get_all())
        available_plans = tuple(plan for plan in plans if plan not in subscribed_plans)
        if not available_plans:
            messagebox.showinfo("Add Subscription", "No available plans to subscribe")
            return

        self._pan_selector = DropdownPublisher(
            self._container,
            "Select the plan you want to add REQUIRED",
            (plan for plan in available_plans),
        )

        self._payment_method_selector = DropdownPublisher(
            self._container,
            "Select the payment method REQUIRED",
            (
                payment_method.get_description()
                for payment_method in self._user.get_payment_methods()
            ),
        )

        self._confirm = DropdownPublisher(
            self._container,
            "We will charge the subscription  REQUIRED",
            (opt for opt in ("Yes", "No")),
        )
        self._confirm.attach(EventListener(self._activate_submit_button))
        self._submit_button.pack()

    def _activate_submit_button(self, confirm: str) -> None:
        self._submit_button.config(state="normal" if confirm == "Yes" else "disabled")

    def _show_informative_banner(self) -> None:
        text = Text(self._container, wrap="word", height=4, bg=Style.BG_COLOR)
        text.insert(
            "end",
            "Add Subscription\n"
            "You can add a subscription to your account by selecting a plan and a payment method. "
            "We will charge the subscription to the selected payment method.",
        )
        text.pack()
        text.config(state="disabled")

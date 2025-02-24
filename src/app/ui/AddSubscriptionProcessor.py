from tkinter import Frame, messagebox, Button
from app.classes.plans import Plan
from app.classes.customers import User
from app.ui.DropdownPublisher import DropdownPublisher


class AddSubscriptionProcessor(Frame):
    def __init__(self, user: User, container: Frame) -> None:
        super().__init__(container)
        self._user = user
        self._container = container
        self._subscriptions = self._user.get_subscriptions()
        self._pan_selector: DropdownPublisher | None = None
        self._payment_method_selector: DropdownPublisher | None = None
        self._confirm: DropdownPublisher | None = None

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
            if self._user.add_subscription(plan, payment_method).get_status() == "ACTIVE":
                messagebox.showinfo("Success", "Subscription added successfully")
            else:
                messagebox.showinfo("Error", "Subscription not added")
        except StopIteration:
            messagebox.showinfo("Error", "Select payment method")

    def _show_add_subscription_form(self) -> None:
        subscribed_plans = self._user.get_user_subscribed_plans()
        plans = (plan.get_name() for plan in Plan.get_all())
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
        Button(self._container, text="Pay", command=self._handle_submit).pack()

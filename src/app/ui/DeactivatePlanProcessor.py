from tkinter import Button, Text, messagebox, Misc
from app.classes.plans import Plan, Subscription

from .DropdownPublisher import DropdownPublisher
from .EventListener import EventListener
from .Style import Style

from collections.abc import Callable


class DeactivatePlanProcessor:
    def __init__(self, container: Misc) -> None:
        self._plans_dropdown: DropdownPublisher | None = None
        self._confirm: DropdownPublisher | None = None
        self._container: Misc = container
        self._submit_button: Button = Button(self._container, text="Deactivate")

    def show_form(self) -> None:
        self._show_informative_banner()
        self._plans_dropdown = DropdownPublisher(
            self._container,
            "Select the plan you want to deactivate",
            lambda _: (_plan.get_name() for _plan in Plan.get_all()),
        )

        deactivation_message = Text(
            self._container, height=2, wrap="word", bg=Style.BG_COLOR, font=Style.FONT
        )
        deactivation_message.insert(
            "end", "Once completed the subscriptions will be inactivated automatically"
        )
        deactivation_message.pack()
        deactivation_message.config(state="disabled")

        self._confirm = DropdownPublisher(
            self._container,
            "Confirm?",
            lambda _: (opt for opt in ("Yes", "No")),
        )

        self._confirm.attach(EventListener(self._show_submit_button))

    def _show_submit_button(self, confirmation: str) -> None:
        self._submit_button.config(
            command=self._deactivate_plan,
            state="normal" if confirmation == "Yes" else "disabled",
        )

        self._submit_button.pack()

    def _deactivate_plan(self) -> Callable[[], None]:
        print(self._plans_dropdown.state, "deactivate")
        plan = Plan.get_plan(self._plans_dropdown.state)
        if not plan:
            messagebox.showerror("Error", "Plan not found")
            return
        inactivate_subscriptions = Subscription.inactivate(plan)
        text = Text(self._container, wrap="word", bg=Style.BG_COLOR, font=Style.FONT)
        text.insert("end", f"The plan {plan.get_name()} has been deactivated")
        text.insert("end", "\n")
        text.insert("end", "Deactivated Subscriptions:")
        text.insert("end", "\n")
        for subscription in inactivate_subscriptions:
            text.insert(
                "end",
                f"Subscription {subscription.get_plan().get_name()} - {subscription.get_user().get_email()}",
            )
            text.insert("end", "\n")
        text.pack()
        text.config(state="disabled")
        self._confirm.clear()
        self._plans_dropdown.clear()

    def _show_informative_banner(self) -> None:
        text = Text(
            self._container, wrap="word", bg=Style.BG_COLOR, height=3, font=Style.FONT
        )
        text.insert(
            "end",
            "Deactivate Plan \n"
            "Select the plan you want to deactivate and confirm the action",
        )
        text.pack()
        text.config(state="disabled")

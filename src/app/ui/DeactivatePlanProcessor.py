from tkinter import Button, Text, messagebox, Misc, Label
from app.classes.plans import Plan, Subscription

from .DropdownPublisher import DropdownPublisher
from .EventListener import EventListener
from .Style import Style
from .EntryInput import EntryInPut
from .Input import Input
from collections.abc import Callable


class DeactivatePlanProcessor:
    def __init__(self, container: Misc) -> None:
        self._plans_dropdown: DropdownPublisher | None = None
        self._container: Misc = container
        self._submit_button: Button = Button(self._container, text="Deactivate")
        self._message: Text = Text(self._container, wrap="word", bg=Style.BG_COLOR, font=Style.FONT)

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
        deactivation_message.config(state="disabled", fg=Style.FG_COLOR)

        expiration_date = Input[str](
            "Ingresa el nombre del plan",
            str,
            _validations=(
                self.validadeconfirmation,
            ),
        )

        label = Label(self._container, text="Ingresa el nombre del plan", bg=Style.BG_COLOR, fg=Style.FG_COLOR, font=Style.FONT)
        label.pack()

        input = EntryInPut(self._container, expiration_date)
        input.pack()
        input.config(fg="black")

        self._show_submit_button()
        
    def validadeconfirmation(self, confirmation: str) -> None:
        if confirmation != self._plans_dropdown.state:
            messagebox.showerror("Error", "Confirmation does not match the plan")
            return

    def _show_submit_button(self) -> None:
        self._submit_button.config(
            command=self._deactivate_plan,
            state="normal",
        )

        self._submit_button.pack()

    def _deactivate_plan(self) -> Callable[[], None]:
        plan = Plan.get_plan(self._plans_dropdown.state)
        if not plan:
            messagebox.showerror("Error", "Plan not found")
            return
        inactivate_subscriptions = Subscription.inactivate(plan)
        text = self._message
        text.config(state="normal")
        text.delete("1.0", "end")
        text.insert("end", "Deactivate Plan")
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
        text.config(fg="white",state="disabled")
        
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
        text.config(state="disabled", fg=Style.FG_COLOR)

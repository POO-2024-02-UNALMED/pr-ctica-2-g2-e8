from app.ui.FieldFrame import FieldFrame
from app.classes.customers import User

from collections.abc import Callable
from tkinter import messagebox, Tk, Menu, Text, Frame
from typing import Literal

from .SubscriptionPaymentProcessor import SubscriptionPaymentProcessor
from .AddSubscriptionProcessor import AddSubscriptionProcessor
from .AddCreditCardProcessor import AddCreditCardProcessor
from .ChangePaymentMethodProcessor import ChangePaymentMethodProcessor
from .DeactivatePlanProcessor import DeactivatePlanProcessor
from .Style import Style


class MainWindow(Tk):
    def __init__(self, user: User, callback: Callable[[None], None]) -> None:
        super().__init__()
        self._callback = callback
        self.geometry("450x550")
        self.title("Payment Manager")
        self._user = user
        self._container = Frame(self, bg=Style.BG_COLOR)
        self.create_menu()
        self._container.pack(fill="both", expand=True)

        initial_message = (
            f"{user.get_email().capitalize()} Welcome to Payment Manager "
            "Please select an option from the menu. "
            "You will find available processes and queries"
            " under the Processes and Queries menu"
        )
        

        text = Text(self._container, wrap="word", bg=Style.BG_COLOR,fg=Style.FG_COLOR, height=4, font=Style.FONT)
        text.insert("1.0", initial_message)
        text.pack()
        text.config(state="disabled")
        self._show_user_subscription()
        self._show_user_credit_cards()

    def _show_user_subscription(self) -> None:
        user_subscriptions = self._user.get_subscriptions()
        text = Text(self._container, wrap="word", bg=Style.BG_COLOR,fg=Style.FG_COLOR, font=Style.FONT)
        text.insert("end", "Subscribed plans \n", "bold", "center")
        text.insert("end", "Plan | Status | Next charge date \n")
        text.insert("end", "-" * 50 + "\n")
        for subs in user_subscriptions:
            text.insert(
                "end",
                (
                    f"{subs.get_plan().get_name()} | {subs.get_status()} | "
                    f"{subs.get_next_charge_date().date().isoformat()}\n"
                ),
            )
            text.insert("end", "-" * 50 + "\n")
        text.pack()
        text.config(state="disabled", height=len(user_subscriptions) * 2 + 3)

    def _show_user_credit_cards(self) -> None:
        user_credit_cards = self._user.get_payment_methods()
        text = Text(self._container, wrap="word", bg=Style.BG_COLOR,fg=Style.FG_COLOR, font=Style.FONT)
        text.insert("end", "Credit cards: \n")
        text.insert("end", "-" * 50 + "\n")
        for card in user_credit_cards:
            text.insert(
                "end",
                f"{card.get_description()}\n",
            )
            text.insert("end", "-" * 50 + "\n")
        text.pack()
        text.config(state="disabled")

    def _go_back_to_welcome(self) -> None:
        self.destroy()
        self._callback()

    def create_menu(self) -> None:
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar)
        file_menu.add_command(label="App", command=self.show_application_info)
        file_menu.add_command(label="Exit", command=self._go_back_to_welcome)
        menu_bar.add_cascade(label="File", menu=file_menu)

        process_menu = Menu(menu_bar)
        functionalities = (
            "Add subscription",
            "Add credit card",
            "Change subscription paying method",
            "Inactivate plan",
            "Pay subscription",
            "Exit",
        )

        for functionality in functionalities:
            process_menu.add_command(
                label=functionality, command=self._handle_selection(functionality)
            )
        menu_bar.add_cascade(label="Processes and Queries", menu=process_menu)

        help_menu = Menu(menu_bar)
        help_menu.add_command(label="About", command=self.show_about_info)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def show_application_info(self) -> None:
        messagebox.showinfo(
            "Payment Manager",
            (
                "Version 1.0\n"
                "Payment Manager is an application designed to "
                "manage subscriptions to service or product plans."
                "The solution focuses on four key aspects: allowing "
                "users to subscribe to plans, enrolling payment methods, "
                "paying for subscriptions, changing payment methods for "
                "subscriptions, and deleting subscriptions. The processing "
                "of transactions, as well as the storage of credit card and "
                "credit card information, will be the responsibility of the "
                "payment gateways, the integration of which can be configured "
                "by the system administrator\n"
            ),
        )

    def list_processes(
        self,
        process: Literal[
            "Add subscription",
            "Add credit card",
            "Change subscription paying method",
            "Inactivate plan",
            "Pay subscription",
            "Exit",
        ],
    ) -> None:
        match process:
            case "Add subscription":
                self.show_add_subscription_form()
            case "Add credit card":
                self.show_add_credit_card_form()
            case "Change subscription paying method":
                self.show_change_payment_method_form()
            case "Inactivate plan":
                self.show_inactivate_plan_form()
            case "Pay subscription":
                self.show_pay_subscription_form()
            case "Exit":
                self.destroy()

    def _clean_container(self) -> None:
        for widget in self._container.winfo_children():
            widget.destroy()

    def _handle_selection(self, process: str) -> Callable[[], None]:
        def _handle_selection() -> None:
            self._clean_container()
            return self.list_processes(process)

        return _handle_selection

    def show_add_credit_card_form(self) -> FieldFrame:
        AddCreditCardProcessor(self._user).show_add_credit_card_form(self._container)

    def show_add_subscription_form(self) -> None:
        AddSubscriptionProcessor(self._user, self._container)

    def show_change_payment_method_form(self) -> None:
        ChangePaymentMethodProcessor(self._user, self._container)

    def show_inactivate_plan_form(self) -> None:
        DeactivatePlanProcessor(self._container).show_form()

    def show_pay_subscription_form(self) -> None:
        SubscriptionPaymentProcessor(self._user, self._container)

    def show_about_info(self) -> None:
        messagebox.showinfo(
            "About",
            (
                "Contact Information\n"
                "Name           - GitHub Username\n"
                "Yeison Liscano - YeisonAndreyLiCe\n"
                "Juan Angel     - JuanPabloAngelZuleta\n"
                "Oscar Rojas    - OkarRojas\n"
            ),
        )

    def run(self) -> None:
        self.mainloop()

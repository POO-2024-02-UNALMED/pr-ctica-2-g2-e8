from app.ui.FieldFrame import FieldFrame
from app.classes.customers import User

from collections.abc import Callable
from tkinter import messagebox, Tk, Menu, Text, Frame
from typing import Literal

from .SubscriptionPaymentProcessor import SubscriptionPaymentProcessor
from .AddSubscriptionProcessor import AddSubscriptionProcessor
from .AddCreditCardProcessor import AddCreditCardProcessor
from .ChangePaymentMethodProcessor import ChangePaymentMethodProcessor

from typing import Final


class MainWindow(Tk):
    _BG_COLOR: Final = "#1d2433"
    def __init__(self, user: User) -> None:
        super().__init__()
        self.geometry("450x450")
        self.title("Payment Manager")
        self._user = user
        self._container = Frame(self, bg=MainWindow._BG_COLOR)
        self.create_menu()
        self._container.pack(fill="both", expand=True)

        initial_message = (
            f"{user.get_email().capitalize()} Welcome to Payment Manager "
            "Please select an option from the menu. "
            "You will find available processes and queries"
            " under the Processes and Queries menu"
        )

        text = Text(self._container, state="normal", wrap="word", height=10)
        text.insert("1.0", initial_message)
        text.pack(fill="both", expand=True)
        text.config(state="disabled")

    def create_menu(self) -> None:
        menu_bar = Menu(self)
        self.config(menu=menu_bar)

        file_menu = Menu(menu_bar)
        file_menu.add_command(label="App", command=self.show_application_info)
        file_menu.add_command(label="Exit", command=self.quit)
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
                self.quit()

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

    def show_inactivate_plan_form(self) -> None: ...
    def show_pay_subscription_form(self) -> None:
        SubscriptionPaymentProcessor(self._user, self._container)

    def _pay_subscription(self, subscription: str, payment_method: str) -> None:
        messagebox.showinfo(
            "Payment",
            f"Subscription {subscription} has been paid using {payment_method}",
        )

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

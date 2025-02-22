from app.ui.Input import Input
from app.ui.FieldFrame import FieldFrame
from app.ui.DropdownPublisher import DropdownPublisher
from app.ui.DropdownObserver import DropdownObserver

from collections.abc import Callable
from tkinter import messagebox, Tk, Menu, StringVar, ttk, X, Label
from typing import Literal
from datetime import datetime


class MainWindow(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.geometry("450x450")
        self.title("Payment Manager")

        self.create_menu()

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
                label=functionality, command=self.list_processes(functionality)
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
    ) -> Callable[[], None]:
        def _list_processes() -> None:
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

        return _list_processes

    def show_add_credit_card_form(self) -> None:
        current_date = datetime.now()
        field_frame = FieldFrame(
            self,
            "Add Credit Card",
            "Please enter the following information to add a new credit card",
            "Add Credit Card",
            "Credit Card Information",
            (
                Input[int](
                    "Card Number",
                    int,
                    _validations=(lambda x: Input.validate_len(str(x), 5, 16),),
                ),
                Input[str](
                    "Expiration Date",
                    str,
                    _validations=(
                        lambda x: Input.validate_len(str(x), 5, 5),
                        lambda x: Input.validate_in_range(int(x[:2]), 1, 12),
                        lambda x: Input.validate_in_range(
                            int(x[3:]), int(str(current_date.year)[2:]), None
                        ),
                    ),
                ),
                Input[int](
                    "Security Code",
                    int,
                    _validations=(lambda x: Input.validate_len(str(x), 3, 5),),
                ),
                Input[str](
                    "Card Holder Name",
                    str,
                    _validations=(lambda x: Input.validate_len(x, 5, 50),),
                ),
            ),
        )
        field_frame.grid(row=0, column=0)

    def show_add_subscription_form(self) -> None: ...
    def show_change_payment_method_form(self) -> None: ...
    def show_inactivate_plan_form(self) -> None: ...
    def show_pay_subscription_form(self) -> None:
        subscriptions = ["Subscription 1", "Subscription 2", "Subscription 3"]
        subscriptions_payment_methods = {
            "Subscription 1": ["Credit Card1", "Debit Card1", "Cash1"],
            "Subscription 2": ["Credit Card2", "Debit Card2", "Cash2"],
            "Subscription 3": ["Credit Card3", "Debit Card3", "Cash3"],
        }

        subscriptions_dropdown = DropdownPublisher(
            self,
            "Select Subscription",
            subscriptions,
        )

        payment_method_dropdown = DropdownPublisher(
            self,
            "Select the payment method",
            [],
        )

        subscriptions_dropdown.attach(
            DropdownObserver(
                payment_method_dropdown,
                lambda subscription: subscriptions_payment_methods.get(
                    subscription, []
                ),
            )
        )

    def _pay_subscription(self, subscription: str, payment_method: str) -> None:
        messagebox.showinfo(
            "Payment",
            f"Subscription {subscription} has been paid using {payment_method}",
        )

    def _show_dropdown(
        self, label: str, values: list[str], callback: Callable[[str], None]
    ) -> tuple[ttk.Combobox, StringVar]:
        selected_value = StringVar()
        Label(self, text=label).pack(fill=X, padx=5, pady=5)
        dropdown = ttk.Combobox(
            self, textvariable=selected_value, values=values, state="readonly"
        )
        dropdown.pack(fill=X, padx=5, pady=5)
        dropdown.bind("<<ComboboxSelected>>", lambda _: callback(selected_value.get()))
        # callback(selected_value.get())
        return dropdown, selected_value

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

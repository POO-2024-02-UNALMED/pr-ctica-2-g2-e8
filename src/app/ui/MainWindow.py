import tkinter as tk
from tkinter import ttk, messagebox
from typing import Literal
from collections.abc import Callable


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        style = ttk.Style()
        style.theme_use("aqua")
        self.geometry("720x720")
        self.title("Payment Manager")

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar)
        file_menu.add_command(label="App", command=self.show_application_info)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        process_menu = tk.Menu(menu_bar)
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
                label=functionality,
                command=self.list_processes(functionality)
            )
        menu_bar.add_cascade(label="Processes and Queries", menu=process_menu)


        help_menu = tk.Menu(menu_bar)
        help_menu.add_command(label="About", command=self.show_about_info)
        menu_bar.add_cascade(label="Help", menu=help_menu)

    def show_application_info(self):
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
            )
        )

    def list_processes(
            self,
            process: Literal[
                "Add subscription",
                "Add credit card",
                "Change subscription paying method",
                "Inactivate plan",
                "Pay subscription",
                "Exit"
            ]
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

    def show_add_credit_card_form(self) -> None:...
    def show_add_subscription_form(self) -> None:...
    def show_change_payment_method_form(self) -> None:...
    def show_inactivate_plan_form(self) -> None:...
    def show_pay_subscription_form(self) -> None:...

    def show_about_info(self):
        messagebox.showinfo(
            "About",
            (
                "Contact Information\n"
                "Name           - GitHub Username\n"
                "Yeison Liscano - YeisonAndreyLiCe\n"
                "Juan Angel     - JuanPabloAngelZuleta\n"
                "Oscar Rojas    - OkarRojas\n"
            )
        )

    def run(self):
        self.mainloop()


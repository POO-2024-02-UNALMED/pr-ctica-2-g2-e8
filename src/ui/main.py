import tkinter as tk
from tkinter import ttk
from typing import Literal


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        style = ttk.Style()
        style.theme_use("aqua")
        style.configure("TButton", background="red")

        self.geometry("720x720")
        self.title("Payment Manager")

        # Menubutton variable
        self.selected_menu_option = tk.StringVar()
        self.selected_menu_option.trace_add("write", self.menu_item_selected)

        self.create_menu()

    def menu_item_selected(self, *_):
        selected_option = self.selected_menu_option.get()

        if selected_option == "Exit":
            self.quit()
        elif selected_option == "Application":
            self.show_app_information()

    def create_menu(self) -> None:
        frame = tk.Frame(self, height=40, padx=10, pady=10, bg="#0d6efd")
        frame.pack(fill=tk.X, side=tk.TOP, anchor=tk.N)

        file_button = self.create_menu_button(frame, "File", ("Application", "Exit"))

        processes_button = self.create_menu_button(
            frame,
            "Processes and Queries",
            (
                "Add subscription",
                "Add credit card",
                "Change subscription paying method",
                "Inactivate plan",
                "Pay subscription",
                "Exit",
            ),
        )

        file_button.place(x=0, y=0)
        processes_button.place(x=100, y=0)

        help_button = tk.Button(frame, text="Help")
        help_button.bind("<Button-1>", self.show_help_window)
        help_button.place(x=320, y=0)

    def create_menu_button(
        self, frame: tk.Frame, label: str, options: tuple[str]
    ) -> ttk.Menubutton:
        menu_button = tk.Menubutton(frame, text=label, bg="#0d6efd", fg="black")
        menu = tk.Menu(menu_button)

        for option in options:
            menu.add_radiobutton(
                label=option, value=option, variable=self.selected_menu_option
            )

        menu_button["menu"] = menu

        return menu_button

    def show_help_window(self, _: tk.Event) -> None:
        title = "Help"
        description = (
            "Contact Information\n"
            "Name\tGitHub Username\n"
            "Yeison Liscano\tYeisonAndreyLiCe\n"
            "Juan Angel\tJuanPabloAngelZuleta\n"
            "Oscar Rojas\tOkarRojas\n"
        )
        self.show_information(title, description, "left")

    def show_app_information(self) -> None:
        title = "Payment Manager"
        description = (
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
        self.show_information(title, description)

    def show_information(
        self,
        title: str,
        description: str,
        justify: Literal["left", "right", "center"] = "center",
    ) -> None:
        app_information_window = tk.Toplevel(self)
        app_information_window.title(title)
        app_information_window.geometry("400x400")
        app_information_window.resizable(False, False)

        app_information_text = tk.Text(app_information_window, wrap=tk.WORD)
        app_information_text.pack(fill=tk.BOTH, expand=True, pady=10, padx=10)
        app_information_text.tag_configure(justify, justify=justify)
        app_information_text.insert(tk.END, description, justify)
        app_information_text.config(state=tk.DISABLED)

        close_button = tk.Button(
            app_information_window, text="Close", command=app_information_window.destroy
        )
        close_button.pack(pady=10)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

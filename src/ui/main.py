import tkinter as tk
from tkinter import ttk


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

    def menu_item_selected(self, *args):
        print(self.selected_menu_option.get(), args)

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
        help_button.bind(
            "<Button-1>", self.show_help_window
        )
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
        # displays a dialog box with help information
        help_window = tk.Toplevel(self)
        help_window.title("Help")
        help_window.geometry("400x400")
        help_window.resizable(False, False)

        help_text = tk.Text(help_window, wrap=tk.WORD)
        help_text.pack(fill=tk.BOTH, expand=True)

        help_text.insert(tk.END, "Contact Information\n")
        # create a table with two columns name ang gitHub username
        help_text.insert(tk.END, "Name\tGitHub Username\n")
        help_text.insert(tk.END, "Yeison Liscano\tYeisonAndreyLiCe\n")
        help_text.insert(tk.END, "Juan Angel\tJuanPabloAngelZuleta\n")
        help_text.insert(tk.END, "Oscar Rojas\tOkarRojas\n")

        close_button = tk.Button(help_window, text="Close", command=help_window.destroy)
        close_button.pack(pady=10)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

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

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

import tkinter as tk
from tkinter.ttk import Style


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        style = Style()
        style.theme_use("aqua")

        self.geometry("720x720")
        self.title("Payment Manager")

        # Menubutton variable
        self.selected_menu_option = tk.StringVar()
        self.selected_menu_option.trace_add("write", self.menu_item_selected)

        self.create_menu()

    def show_window_1(self) -> None:...

    def show_window_2(self) -> None:...

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()

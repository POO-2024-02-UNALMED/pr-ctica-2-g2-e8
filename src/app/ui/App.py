from app.classes.customers import User
from app.classes import WithId
from app.database import Repository
from tkinter import Tk, messagebox
from .FieldFrame import FieldFrame
from .MainWindow import MainWindow
from .Input import Input
from typing import cast


class App:
    print("App")
    def __init__(self) -> None:
        self.show_login_window()

    def show_window_1(self, user_name: str, password: str) -> None:
        user = Repository.load("User", WithId.create_id(user_name, password))
        if not user:
            messagebox.showerror("Error", "User not found")
            return self.show_login_window()

        MainWindow(cast(User, user)).run()

    def show_window_2(self) -> None: ...

    def show_login_window(self) -> None:
        window = Tk()
        window.geometry("400x400")
        window.title("Login")
        user_name = Input[str]("UserName", str)
        password = Input[str]("Password", str)
        login_frame = FieldFrame(
            window,
            "Login",
            "Add your credentials",
            "Credential",
            "Value",
            (user_name, password),
        )
        login_frame.pack()

        def _close() -> None:
            window.destroy()
            self.show_window_1(user_name.get_value(), password.get_value())

        login_frame.get_submit_button().config(command=_close)
        window.mainloop()

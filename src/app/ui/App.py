from app.classes.customers import User
from app.classes import WithId
from app.database import Repository
from tkinter import Tk, messagebox
from .FieldFrame import FieldFrame
from .MainWindow import MainWindow
from .WelcomeWindow import WelcomeWindow
from .Input import Input
from typing import cast


class App:
    def __init__(self) -> None:
        self._show_welcome_window()

    def _show_main_window(self, user_name: str, password: str) -> None:
        user = Repository.load("User", WithId.create_id(user_name, password))
        if not user:
            messagebox.showerror("Error", "User not found")
            return self._show_login_window()

        MainWindow(cast(User, user), self._show_welcome_window).run()

    def _show_welcome_window(self) -> None:
        WelcomeWindow(self._show_login_window).run()

    def _show_login_window(self) -> None:
        window = Tk()
        window.geometry("310x270")
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
            self._show_main_window(
                user_name.get_initial_value(), password.get_initial_value()
            )

        login_frame.get_submit_button().config(command=_close)
        window.mainloop()

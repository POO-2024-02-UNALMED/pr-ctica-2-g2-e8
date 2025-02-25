from .MainWindow import MainWindow
from .WelcomeWindow import WelcomeWindow

from app.classes.customers import User
from app.database import Repository
from app.database.Loader import Loader

from typing import cast


class App:
    def __init__(self, loader: Loader) -> None:
        self._loader = loader

    def _show_main_window(self) -> None:
        user = Repository.load("User", self._loader.get_system_user().get_id())
        MainWindow(cast(User, user), self._show_welcome_window).run()

    def _show_welcome_window(self) -> None:
        WelcomeWindow(self._show_main_window).run()

    def run(self) -> None:
        self._show_welcome_window()

from app.ui import App
from app.database.Loader import Loader
from app.ui.WelcomeWindow import MainWindow

if __name__ == "__main__":
    loader = Loader("email", "password", True)
    loader.load_data()
    window = MainWindow()
    window.run()
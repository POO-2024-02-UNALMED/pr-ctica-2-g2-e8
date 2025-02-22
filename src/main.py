from app.ui import MainWindow
from app.database.Loader import Loader

if __name__ == "__main__":
    loader = Loader("email", "password", True)
    loader.load_data()
    window = MainWindow()
    window.run()

    # bad practice: it will execute only by importing
    # from app.ui import WelcomeWindow
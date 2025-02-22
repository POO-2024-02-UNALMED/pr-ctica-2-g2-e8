from app.ui import App
from app.database.Loader import Loader

if __name__ == "__main__":
    loader = Loader("email", "password", True)
    loader.load_data()
    app = App()

    # bad practice: it will execute only by importing
    # from app.ui import WelcomeWindow
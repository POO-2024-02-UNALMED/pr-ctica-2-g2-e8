from app.ui import App
from app.database.Loader import Loader

if __name__ == "__main__":
    loader = Loader("doe@gmail.com", "password", False)
    loader.load_data()
    App()